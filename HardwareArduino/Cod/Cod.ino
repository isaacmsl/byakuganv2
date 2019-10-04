//#include "Estrategia.h"
#include <ros.h>
#include <robo_hardware2.h>
#include <byakugan/BotoesMsg.h>

//Estrategia estrategia;

byakugan::BotoesMsg dataBtns;
ros::Publisher pubBtns("botoes_init", &dataBtns);

ros::NodeHandle nh;

void setup(){
  //Serial.begin(9600);
  robo.configurar(false);
  //robo.habilitaTCS34();
  //estrategia.calibrar();

  nh.getHardware()->setBaud(115200);
  nh.initNode();
  nh.advertise(pubBtns);

}

void loop(){
  dataBtns.botao1.data = robo.botao1Pressionado();
  dataBtns.botao2.data = robo.botao2Pressionado();
  dataBtns.botao3.data = robo.botao3Pressionado();
  pubBtns.publish(&dataBtns);
  nh.spinOnce();
  //estrategia.executar();
}

//angelo.reset(obr2020, true);**-123
