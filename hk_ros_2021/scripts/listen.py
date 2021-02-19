#!/usr/bin/env python
import rospy 
import yaml
import rospkg

#from std_msgs.msg import String


def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
def listen():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listen', anonymous=True)

    rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


object_list = []

object_list.append( {"obj_type": "A", "XY_pos": [30.756,32.332]} )
object_list.append( {"obj_type": "A", "XY_pos": [20.756,39.332]} )
object_list.append( {"obj_type": "A", "XY_pos": AprilTagDetectionArray[0] } )

filename = "latest_output_file.yaml"
filepath = rospkg.RosPack().get_path('hk_ros_2021') + '/exported_detection_logs/'

with open(filepath + filename, 'w') as outfile:
    yaml.dump_all(object_list, outfile,explicit_start=True)

if __name__ == '__main__':
    listen()
