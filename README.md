# Byakugan: Visão Computacional

![Contributions](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)
 ![License](https://img.shields.io/github/license/PauloVLB/byakuganv2)

- [Resumo](#resumo)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Resultados](#resultados)
    - [Premiação OBR 2019](#premiação-obr-2019)
    - [Premiação MNR 2019](#premiação-mnr-2019)
- [Mais Detalhes](#mais-detalhes)
- [Autores](#autores)

## Resumo

A Olimpíada Brasileira de Robótica (OBR) propõe
que seus participantes desenvolvam um robô capaz de superar
desafios, de forma autônoma. Com a intenção de resolver um
desses desafios, este trabalho propõe a utilização de tecnologias
de reconhecimento e tratamento de imagem. Procurando utilizar
uma forma alternativa ao que geralmente é proposto para a
competição da OBR, foi adicionada uma câmera em um robô,
que visa adquirir imagens do ambiente onde estão dispostas as
vítimas (representadas por bolas) e uma área para resgate (área triangular elevada) (**Figuras 1 e 2**). Utilizando o Robotic Operating
System (ROS), foram realizadas algumas tarefas no robô, tais
como: a utilização de outros sensores além da câmera, o
acionamento de atuadores presentes no robô e o processamento
das imagens, feito com a biblioteca OpenCV. Os testes iniciais
indicam resultados promissores para a estratégia de
identificação de vítimas e da área de resgate. 

[Mais Detalhes](#mais-detalhes)


## Tecnologias utilizadas

- [Python](https://www.python.org/) - Linguagem de programação para o middleware ROS;
- [ROS](http://wiki.ros.org/pt_BR/ROS/Tutorials) - Middleware para comunicação Arduino/Raspberry;
- [C++](https://www.cplusplus.com/) - Linguagem de programação para o microcontrolador Arduino;
- [Arduino](https://www.arduino.cc/) - Microcontrolador para os componentes eletrônicos;
- [OpenCV](https://opencv.org/) - Biblioteca de reconhecimento e tratamento de imagens;
- [Raspberry PI](https://www.raspberrypi.org/) - Microprocessador para processamento das imagens;
- [Trello](https://trello.com/pt-BR) - Organização do trabalho.

## Resultados

### Detecção de vítimas e área de resgate
Como o resultado o projeto mostrou-se promissor na detecção de círculos (vítimas) e retângulos (visão frontal da área de resgate).

Apesar das dificuldades encontradas, como: 
poluição visual; iluminação; profundidade; processamento saturado (imagens de alta qualidade); falhas de comunicação Arduino/Raspberry; problemas com hardware; foi possível alcançar um nível relevante na identificação das vítimas e área de resgate (**Figuras 1 e 2**).


<div width="50%" style="text-align: center">
<img src="https://user-images.githubusercontent.com/31678236/94749031-2e60ca80-0359-11eb-9049-096aa08827b0.png" width="100%" style="object-fit: cover; object-position: center;">

**Figura 1 - Detecção de vítima viva (prateada) e morta (escura) com diferentes profundidades**
</div>

<div width="50%" style="text-align: center">
<img src="https://user-images.githubusercontent.com/31678236/94749105-58b28800-0359-11eb-8210-e70448c1d756.png" width="100%" style="object-fit: cover; object-position: center;">

**Figura 2 - Detecção da área de resgate com vítima prateada
obstruindo a visão**
</div>

### Premiação OBR 2019

Na OBR do ano de 2019, esse projeto foi contemplado com o prêmio extra de "Inovação" por ser o único robô da competição utilizando tecnologias de tratamento e processamento de imagens. O robô do projeto foi utilizado pela [equipe Wall-E](https://github.com/IFRN-SC/Wall-E-2018-) do IFRN Campus Santa Cruz (**Figura 3**).

<img src="https://user-images.githubusercontent.com/31678236/94749507-556bcc00-035a-11eb-92fa-9905a9b58741.png" width="100%">

**Figura 3 - Robô Wall-E com crachá de participação e medalha de premiação.**

### Premiação MNR 2019

Esse projeto foi convidado a participar da Mostra Nacional de Robótica (MNR) 2019, sediada na cidade de Rio Grande, RS. Como resultado da apresentação, foi premiado como um dos projetos destaque, recebendo por isso, a proposta de Bolsa de Iniciação Científica Júnior (ICJr) (**Figura 4**).

<img src="https://user-images.githubusercontent.com/31678236/94750097-b6e06a80-035b-11eb-89d3-043c8cb9df8e.png" width="100%">

**Figura 4 - Integrantes do projeto e avaliador da MNR 2019**

## Mais Detalhes

- [Relatório Científico](https://github.com/isaacmsl/byakuganv2/files/5308945/relatorio_expotec_byakugan.docx.pdf)

- [Artigo Científico Publicado na MNR 2019](http://200.145.27.212/MNR/mostravirtual/interna.php?id=32678)


## Autores

| [<img src="https://avatars3.githubusercontent.com/u/31693006?s=460&v=4" width=115><br><sub>@isaacmsl</sub>](https://github.com/isaacmsl) | [<img src="https://avatars3.githubusercontent.com/u/31678236?s=400&v=4" width=115><br><sub>@PauloVLB</sub>](https://github.com/PauloVLB) | [<img src="https://avatars3.githubusercontent.com/u/40503734?s=400&v=4" width=115><br><sub>@doug3321</sub>](https://github.com/doug3321) | [<img src="https://avatars3.githubusercontent.com/u/4775968?s=400&v=4" width=115><br><sub>@lennedy</sub>](https://github.com/lennedy) |
| :---: | :---: | :---: | :---: |

