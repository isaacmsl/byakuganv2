#include <robo_hardware2.h>
#include <ros.h>
#include <std_msgs/Int32MultiArray.h>
#include <byakugan/RefletanciaMsg.h>
#include <byakugan/BotoesMsg.h>
#include <byakugan/SensoresDistanciaMsg.h>
//#include <byakugan/LedMsg.h>

byakugan::RefletanciaMsg dataRefletancia;
ros::Publisher pubRefletancia("refletancia", &dataRefletancia);

byakugan::BotoesMsg dataBtns;
ros::Publisher pubBtns("botoes_init", &dataBtns);

byakugan::SensoresDistanciaMsg dataDist;
ros::Publisher pubDist("distancia", &dataDist);


ros::NodeHandle nh;
/*
#define LED_SERVO1 2
#define LED_SERVO2 3
*/
void motoresCb(const std_msgs::Int32MultiArray &motores){
  robo.acionarMotores(motores.data[0], motores.data[1]);
}
ros::Subscriber<std_msgs::Int32MultiArray> subMotores("ctrl_motores", &motoresCb);



void garraCb(const std_msgs::Int32MultiArray &garra){
  robo.acionarServoGarra1(garra.data[0]);
  robo.acionarServoGarra2(garra.data[1]);
}

ros::Subscriber<std_msgs::Int32MultiArray> subGarras("ctrl_garras", &garraCb);

/*
void ledsCb(const byakugan::LedMsg &leds){
  robo.setEstadoLed(1, leds.led1.data);
  robo.setEstadoLed(2, leds.led2.data);
  robo.setEstadoLed(3, leds.led3.data);
}

ros::Subscriber<byakugan::LedMsg> subLeds("ctrl_leds", &ledsCb);
*/

void setup() {

  nh.getHardware()->setBaud(115200);
  nh.initNode();

  //pinMode(LED_BUILTIN, OUTPUT);

  //pinMode(LED_SERVO1, OUTPUT);
  //pinMode(LED_SERVO2, OUTPUT);

  nh.subscribe(subMotores);
  //nh.subscribe(subLeds);
  nh.subscribe(subGarras);

  nh.advertise(pubRefletancia);
  nh.advertise(pubDist);
  nh.advertise(pubBtns);
  
  robo.configurar(true);
  robo.acionarServoGarra2(100);
  robo.acionarServoGarra1(75);
  //robo.habilitaTCS34(); 
}

void loop() {
  
  dataRefletancia.refletancia[0] = robo.lerSensorLinhaMaisEsqSemRuido();
  dataRefletancia.refletancia[1] = robo.lerSensorLinhaEsqSemRuido();

  
  dataRefletancia.refletancia[2] = robo.lerSensorLinhaDirSemRuido();
  dataRefletancia.refletancia[3] = robo.lerSensorLinhaMaisDirSemRuido();

  dataBtns.botao1.data = robo.botao1Pressionado();
  dataBtns.botao2.data = robo.botao2Pressionado();
  dataBtns.botao3.data = robo.botao3Pressionado();

  dataDist.sensoresDistancia[0] = robo.lerSensorSonarFrontal();
  dataDist.sensoresDistancia[1] = robo.lerSensorSonarDir();
  dataDist.sensoresDistancia[2] = robo.lerSensorSonarEsq();

  pubRefletancia.publish(&dataRefletancia);
  pubDist.publish(&dataDist);
  pubBtns.publish(&dataBtns);

  nh.spinOnce();

}
