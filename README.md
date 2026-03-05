# OpenShift Auto-Scaling Demo on IBM Z (s390x) Mainframe || LinuxONE

Este repositório contém uma Prova de Conceito (PoC) prática demonstrando o **Horizontal Pod Autoscaler (HPA)** do Red Hat OpenShift rodando nativamente na arquitetura **IBM Z e LinuxONE (s390x)**.

O objetivo deste laboratório é ilustrar a elasticidade da plataforma. Uma aplicação Python/Flask é estressada artificialmente usando o `k6`, forçando o OpenShift a provisionar novos pods dinamicamente para lidar com o pico de consumo de CPU.

## 🛠️ Tecnologias Utilizadas
* **Plataforma:** Red Hat OpenShift Container Platform (Arquitetura s390x)
* **Linguagem:** Python 3.9 (via Red Hat UBI 8)
* **Orquestração:** Kubernetes HPA (Horizontal Pod Autoscaler)
* **Load Testing:** Grafana k6

## 📂 Estrutura do Projeto
* `app.py`: Aplicação Flask com uma rota `/load` projetada para consumir CPU intencionalmente.
* `requirements.txt`: Dependências do Python.
* `Dockerfile`: Instruções de build usando a imagem Universal Base Image (UBI) otimizada.
* `infra.yaml`: Manifestos Kubernetes (Deployment, Service, Route e HPA).
* `loadtest.js`: Script do k6 para simulação de injeção de usuários simultâneos.

---

## Como Executar o Laboratório

### Pré-requisitos
1. Acesso a um cluster OpenShift (preferencialmente rodando em nós s390x para o contexto completo da demo).
2. CLI do OpenShift (`oc`) instalada e autenticada.
3. k6 instalado na sua máquina local.

### Passo 1: Clone o repositório
git clone https://github.com/SEU_USUARIO/openshift-hpa-ibmz.git
cd openshift-hpa-ibmz

### Passo 2: Build da Imagem (Direct to Cluster)
Para evitar a necessidade de um registry externo ou emuladores multi-arch na máquina local, faremos um **Binary Build** direto no cluster OpenShift.

Crie o BuildConfig:
oc new-build --name=demo-autoscale --binary --strategy=docker

Inicie o build enviando os arquivos locais:
oc start-build demo-autoscale --from-dir=. --follow
*(Aguarde o status de sucesso do build. A imagem estará disponível no ImageStream `demo-autoscale:latest`)*.

### Passo 3: Deploy da Infraestrutura
**Atenção:** Antes de aplicar, edite o arquivo `infra.yaml`. Na linha `image:` do Deployment, certifique-se de que o caminho aponta para o registry interno do seu projeto:
`image-registry.openshift-image-registry.svc:5000/NOME_DO_SEU_PROJETO/demo-autoscale:latest`

Aplique os recursos no cluster:
oc apply -f infra.yaml

Obtenha a URL da aplicação gerada pela Route e atualize a variável `url` dentro do arquivo `loadtest.js`.

---

## 📊 Executando a Demonstração (Split-Screen)
Para o melhor efeito visual durante uma apresentação, abra 3 terminais lado a lado na sua máquina:

**Terminal 1 (Monitorando os Pods):**
watch -n 1 oc get pods -l app=demo-autoscale

**Terminal 2 (Monitorando o HPA):**
watch -n 1 oc get hpa demo-hpa

**Terminal 3 (Execução do Teste de Carga):**
k6 run loadtest.js

### O que você vai observar:
1. O `k6` começará a injetar carga na rota `/load`.
2. No Terminal 2, a métrica de CPU (TARGETS) ultrapassará a marca de `50%`.
3. O OpenShift reagirá provisionando novas réplicas (escala de 1 até 10 pods) visíveis no Terminal 1.
4. Quando o teste finalizar, o ambiente passará por um período de *cool-down* e reduzirá automaticamente os pods de volta para 1.

---

## 🧹 Limpeza (Clean Up)
Para remover todos os recursos criados por esta demo no seu cluster:
oc delete all -l app=demo-autoscale
oc delete hpa demo-hpa

---
*Desenvolvido para demonstrações de arquitetura Fit-for-Purpose no ecossistema z/LinuxONE.*
