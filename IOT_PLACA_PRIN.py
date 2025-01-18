import psycopg2
from datetime import datetime
import paho.mqtt.client as mqtt
import asyncio
import smtplib
import email.message


# Definir configurações do banco de dados
database_config = { 
    "host": "sensor-check.c3y8eoi0a1dx.us-east-1.rds.amazonaws.com",
    "user": "postgres",
    "port": 5432,
    "database": "postgres",  # Set your database name
    "password": "SCheck7890",
    "options": "-c client_encoding=utf8"
}

data_alerta = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
# Inicialize as variáveis globais
limite_superior_temp = None
limite_inferior_temp = None
limite_superior_umi = None
limite_inferior_umi = None

def carregar_configuracoes():
    global limite_superior_temp, limite_inferior_temp, limite_superior_umi, limite_inferior_umi
    try:
        # Conectar ao banco de dados
        conn = psycopg2.connect(**database_config)
        cur = conn.cursor()

        # Executar a consulta SQL para obter as configurações
        cur.execute("SELECT min_temp, max_temp, min_ur, max_ur FROM configuracoes ORDER BY id DESC LIMIT 1")
        configuracoes = cur.fetchone()

        if configuracoes:
            # Atualizar as variáveis com as configurações do banco de dados
            limite_inferior_temp, limite_superior_temp, limite_inferior_umi, limite_superior_umi = configuracoes
            print('Configurações carregadas do banco de dados com sucesso.')
        else:
            print('Nenhuma configuração encontrada no banco de dados.')

    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)

    finally:
        # Fechar a conexão com o banco de dados
        if conn is not None:
            cur.close()
            conn.close()

# Executar a função para carregar as configurações
carregar_configuracoes()

# Store latest readings
latest_readings = {
    "SalaDeEstar": {"temperatura": None, "umidade": None, "timestamp": None},
    "Quarto": {"temperatura": None, "umidade": None, "timestamp": None}
}

def send_email(subject, body):
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = 'equipeSensorCheck@gmail.com'
    msg['To'] = 'clientesensorcheck@gmail.com'
    password = 'cpis jzng mbdz ajfy'
    msg.set_payload(body)
    
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    s.quit()
    print('Email enviado')

def email_temperatura(temperatura, comodo):
    corpo_email = f'''
    Prezado,
        No dia/hora {data_alerta} o valor da temperatura foi de {temperatura} no cômodo {comodo}, diferindo dos valores aceitáveis.
        Recomendamos a verificação do ambiente.
        Att,
        equipe SensorCheck'''
    send_email("ALERTA! Temperatura acima do limite", corpo_email)

def email_umidade(umidade, comodo):
    corpo_email = f'''
    Prezado,
        No dia/hora {data_alerta} o valor de umidade foi de {umidade} no cômodo {comodo}, diferindo dos valores aceitáveis.
        Recomendamos a verificação do ambiente.
        Att,
        equipe SensorCheck'''
    send_email("ALERTA! Umidade acima do limite", corpo_email)

# Definir clientes MQTT
client1 = mqtt.Client(client_id="SensorCheck3")
client1.username_pw_set("SensorCheck3", "123456789")

client2 = mqtt.Client(client_id="SensorCheck2")
client2.username_pw_set("SensorCheck2", "123456789")

# Definir callbacks para os clientes MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    if client == client1:
        client.subscribe("Umidade3")
        client.subscribe("Temperatura3")
    elif client == client2:
        client.subscribe("Umidade2")
        client.subscribe("Temperatura2")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = float(msg.payload.decode('utf-8'))
    print(f"Received message on topic {topic}: {payload}")

    # Determine the room based on the client
    comodo = "SalaDeEstar" if client == client1 else "Quarto"
    data_e_hora = datetime.now()

    # Check the limits and send an email if necessary
    if "Umidade" in topic:
        if payload > limite_superior_umi or payload < limite_inferior_umi:
            email_umidade(payload, comodo)
        latest_readings[comodo]["umidade"] = payload
    elif "Temperatura" in topic:
        if payload > limite_superior_temp or payload < limite_inferior_temp:
            email_temperatura(payload, comodo)
        latest_readings[comodo]["temperatura"] = payload
    
    # Update the timestamp for the latest reading
    latest_readings[comodo]["timestamp"] = data_e_hora

    # Insert data into the database if both temperature and humidity readings are available
    if latest_readings[comodo]["temperatura"] is not None and latest_readings[comodo]["umidade"] is not None:
        try:
            conn = psycopg2.connect(**database_config)
            cur = conn.cursor()
            cur.execute(
                f"INSERT INTO {comodo} (data_e_hora, umidade, temperatura) VALUES (%s, %s, %s)",
                (latest_readings[comodo]["timestamp"], latest_readings[comodo]["umidade"], latest_readings[comodo]["temperatura"])
            )
            latest_readings[comodo]["umidade"] = None
            latest_readings[comodo]["temperatura"] = None
            conn.commit()
            print(f"Dados inseridos na tabela {comodo}")
            # Reset the latest readings after insertion
            latest_readings[comodo]["temperatura"] = None
            latest_readings[comodo]["umidade"] = None
        except psycopg2.Error as e:
            print("Erro ao conectar ao banco de dados:", e)
        finally:
            if conn:
                cur.close()
                conn.close()

# Configurar callbacks para os clientes MQTT
client1.on_connect = on_connect
client1.on_message = on_message

client2.on_connect = on_connect
client2.on_message = on_message

# Conectar aos brokers MQTT
client1.connect("broker.emqx.io", 1883)
client2.connect("broker.emqx.io", 1883)

# Função para reiniciar os loops dos clientes a cada 30 segundos
async def restart_loops():
    while True:
        await asyncio.sleep(30)  # Aguardar 30 segundos
        client1.loop_stop()  # Parar loop do client1
        client2.loop_stop()  # Parar loop do client2
        client1.loop_start()  # Iniciar loop do client1
        client2.loop_start()  # Iniciar loop do client2

# Iniciar loop para reiniciar os loops dos clientes
asyncio.run(restart_loops())

# Manter a execução dos clientes MQTT em threads separadas
client1.loop_forever()
client2.loop_forever()
