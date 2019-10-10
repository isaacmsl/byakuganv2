#include "ros/ros.h"
#include "std_msgs/Empty.h"

#include <sstream>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "acionar");
  //oi
  ros::NodeHandle n;
  ros::Publisher pub = n.advertise<std_msgs::Empty>("ctrl", 1000, true);

  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::Empty msg;

    pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }


  return 0;
}