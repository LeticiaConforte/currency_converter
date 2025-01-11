# Conversor de Moedas em Python

## Descrição
Este projeto é um **Conversor de Moedas** desenvolvido em Python com interface gráfica. Ele permite realizar conversões de moedas usando taxas de câmbio obtidas em tempo real por meio de uma API. O projeto possui funcionalidades avançadas, como suporte a múltiplos idiomas, gráficos para visualizar flutuações de câmbio e cache para reduzir chamadas à API.

## Funcionalidades
- **Conversão de moedas**: Calcule o valor convertido entre diferentes moedas.
- **Gráficos de flutuação**: Visualize as taxas de câmbio de uma moeda base em relação a outras.
- **Histórico de conversões**: Armazene e exiba conversões anteriores.
- **Suporte a múltiplos idiomas**:
  - Português
  - Inglês
  - Espanhol
  - Francês
- **Cache de dados**: Reduz chamadas à API armazenando taxas de câmbio por até 30 minutos.

## Tecnologias Utilizadas
- **Python 3**
- Bibliotecas:
  - `requests`: Para acessar a API de câmbio.
  - `tkinter`: Para a interface gráfica.
  - `matplotlib`: Para criar gráficos de flutuação.
  - `time`: Para gerenciar o cache.

## Como Executar

1. **Pré-requisitos**:
   - Python 3 instalado no sistema.
   - Instalar as bibliotecas necessárias:
     ```bash
     pip install requests matplotlib
     ```

2. **Configurar a API Key**:
   - Obtenha uma chave da [ExchangeRate API](https://open.er-api.com/).
   - Substitua o valor `"sua_api_key_aqui"` no código pela sua chave.

3. **Executar o Código**:
   - Rode o script Python:
     ```bash
     python currency_converter.py
     ```

## Uso
1. **Converter moedas**:
   - Insira o valor no campo apropriado.
   - Escolha as moedas de origem e destino.
   - Clique em **Converter** para exibir o resultado.

2. **Atualizar taxas de câmbio**:
   - Clique no botão **Atualizar Taxas** para obter os dados mais recentes.

3. **Visualizar flutuações de câmbio**:
   - Selecione uma moeda base.
   - Clique em **Exibir Flutuações** para abrir o gráfico.

4. **Selecionar idioma**:
   - Use o menu "Language / Idioma" para alternar entre os idiomas disponíveis.

## Estrutura do Código
- **Interface gráfica**: Desenvolvida com `Tkinter`.
- **Conexão com a API**: Implementada com `requests` para buscar as taxas de câmbio.
- **Gráficos de flutuação**: Criados usando `matplotlib`.
- **Cache**: Utiliza um dicionário com timestamp para armazenar as taxas por 30 minutos.

## Melhorias Futuras
- Adicionar suporte para personalizar os idiomas disponíveis.
- Permitir seleção de moedas diretamente no gráfico.
- Implementar salvamento do histórico em arquivos CSV.

---

**Autor**: Este projeto foi desenvolvido para fins didáticos e de aprendizado em Python e APIs.

**Licença**: MIT

