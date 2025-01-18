# Sistema de Monitoramento de Temperatura e Umidade com IoT

Este projeto visa desenvolver um sistema inteligente para monitoramento contínuo e em tempo real de temperatura e umidade, utilizando a combinação de placas ESP-32 e ESP-01, com comunicação Wi-Fi e integração com a Internet das Coisas (IoT). O sistema coleta dados ambientais e permite a gestão automatizada do ambiente, garantindo maior eficiência e segurança.

## Sumário

1. [Descrição do Sistema](#descrição-do-sistema)
2. [Escopo do Projeto](#escopo-do-projeto)
3. [Descrição do Ambiente](#descrição-do-ambiente)
4. [Detalhamento das Etapas Realizadas](#detalhamento-das-etapas-realizadas)
    - [Código em Python da Placa Principal](#código-em-python-da-placa-principal)
    - [Funcionamento dos Sensores](#funcionamento-dos-sensores)

---

## Descrição do Sistema

O sistema foi projetado utilizando as placas **ESP-32** para comunicação com a internet e **ESP-01** para a leitura dos sensores de temperatura e umidade, representando uma aplicação prática de **Internet das Coisas (IoT)**. A integração entre essas placas permite a criação de um sistema inteligente que coleta e monitora dados ambientais em tempo real, utilizando um **Broker MQTT** online hospedado na plataforma **Amazon AWS**.

Essa comunicação possibilita a coleta e armazenamento dos dados em um banco de dados, o que auxilia na tomada de decisões automatizadas para otimizar as condições climáticas do ambiente. O controle remoto das condições pode ser implantado em **ambientes internos e externos**, oferecendo maior eficiência na gestão de recursos e processos.

---

## Escopo do Projeto

O escopo do projeto inclui o desenvolvimento e a implementação de um **sistema de monitoramento de temperatura e umidade em tempo real**. Este sistema será capaz de:

- **Capturar dados precisos** de temperatura e umidade e transmiti-los para uma plataforma de visualização.
- **Integrar alertas automatizados** para notificar os usuários sobre variações indesejadas nos níveis de temperatura e umidade.
- **Exibir as leituras** de temperatura e umidade em tempo real, com atualizações a cada 30 segundos.
- **Enviar alertas** caso os níveis de temperatura estejam fora dos limites predefinidos, permitindo que o usuário tome ações corretivas.
- **Permitir que o usuário ajuste** o intervalo de temperatura em que deseja receber alertas.
- **Mostrar histórico de dados** para análise da evolução das condições ambientais.
- **Garantir segurança** nas informações medidas, com acesso restrito apenas aos usuários autorizados.

O sistema será acessível via um **aplicativo intuitivo** e fácil de usar, compatível com **iOS** e **Android**. O aplicativo funcionará de forma confiável, mesmo com **conectividade intermitente**. Ele também assegurará que as leituras de temperatura estejam dentro de uma **margem de erro aceitável**, conforme as limitações dos sensores.

O objetivo principal é fornecer aos usuários uma ferramenta eficaz para **manter as condições ideais** nos ambientes internos, minimizando riscos de danos à propriedade.

---

## Descrição do Ambiente

O sistema será implementado em **uma casa com múltiplos cômodos**, utilizando a distribuição estratégica de sensores conectados a uma rede central de comunicação. As principais tecnologias envolvidas são:

- **Placas ESP8266** programadas em **C** e simuladas através do **simulador Wokwi**.
- **Broker MQTT** hospedado na **Amazon AWS**.
- **Banco de dados (BC)** para o armazenamento e processamento dos dados coletados.

Além disso, a plataforma de software será desenvolvida para permitir a visualização dos dados, acessível aos usuários finais por meio de dispositivos móveis.

---

## Detalhamento das Etapas Realizadas

### 1. Levantamento de Requisitos

Foram realizadas reuniões com os **stakeholders** para entender os requisitos específicos do sistema, como:

- **Precisão dos sensores**.
- **Frequência de amostragem** dos dados.
- **Critérios de alerta**.
- **Requisitos de interface** do usuário.

### 2. Projeto de Arquitetura do Sistema

Desenvolvimento da arquitetura do sistema, que inclui:

- **Seleção e posicionamento dos sensores**.
- **Infraestrutura de rede** necessária.
- **Interface de usuário** para o acesso e controle do sistema.

### 3. Desenvolvimento de Hardware e Software

- Implementação dos componentes **físicos do sistema** (sensores de temperatura e umidade, dispositivos de comunicação, servidores de dados).
- Desenvolvimento do **software** para a coleta, transmissão, armazenamento e visualização dos dados.

#### 3.1 Código em Python da Placa Principal

O código em Python da placa principal é responsável por coordenar a **coleta e interpretação dos dados** dos sensores de temperatura e umidade, garantindo o funcionamento do sistema.

#### 3.2 Funcionamento dos Sensores

Os **sensores** enviados pela **placa ESP-01** fornecem os dados necessários para o código Python na **placa principal**, que acessa e interpreta essas informações, permitindo a análise e o monitoramento contínuo das condições ambientais.

---

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
