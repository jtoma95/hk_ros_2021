#!/usr/bin/env python
#import rospy 
#import yaml
#import rospkg
#import tf
#import tf_conversions
#from apriltag_ros.msg import AprilTagDetectionArray

import rospy
import rospkg
import yaml
import math
import tf
import geometry_msgs.msg
from std_msgs.msg import String
from apriltag_ros.msg import AprilTagDetectionArray



rospy.init_node('listen', anonymous=True)

global transform
transform = tf.TransformListener()



class Object():
	
		def __init__(self, tag_id = None, tag_frame = None, obj_type = None, x_pos = None, y_pos = None):
					
				self.tag_id = tag_id
				self.tag_frame = tag_frame
				self.obj_type = obj_type
				self.x_pos = x_pos
				self.y_pos = y_pos

				


def callback(data):

		if(len(data.detections) != 0):
				
				new_obj = Object()
				new_obj.obj_type = "A"
				new_obj.tag_id = str(data.detections[0].id[0])
				new_obj.tag_frame = "tag_"+new_obj.tag_id
				transform.waitForTransform('/static_frame', new_obj.tag_frame, rospy.Time(), rospy.Duration(1))
				(trans,rot) = transform.lookupTransform('/static_frame',new_obj.tag_frame,rospy.Time())
				#transform.waitForTransform('/map', new_obj.tag_frame, rospy.Time(), rospy.Duration(1))
				#(trans,rot) = transform.lookupTransform('/map',new_obj.tag_frame,rospy.Time())
				new_obj.x_pos = trans[0]
				new_obj.y_pos = trans[1]


				object_typeA[new_obj.tag_frame] = ([new_obj.x_pos,new_obj.y_pos])
				print(str(new_obj.tag_frame) + " : " + str(object_typeA[new_obj.tag_frame]))
		
				
		
						

def listen():
		

		rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback)
		
		rospy.spin()


object_typeA = {}
object_list = []


		
if __name__ == '__main__':
		listen()
		filename = "latest_output_file.yaml"
		filepath = rospkg.RosPack().get_path('hk_ros_2021') + '/exported_detection_logs/'

		for key, value in object_typeA.items():
				object_list.append( {"obj_type": "A", "XY_pos": value} )
				print(key, value)

		with open(filepath + filename, 'w') as outfile:
				yaml.dump_all(object_list, outfile,explicit_start=True)
				#yaml.dump(object_list, outfile,default_flow_style=False)

				print("DONE")

#TO DO: 
#import yolo algortihm 
#rospy.Subscriber("/yolo thing", yoloy thing thing , callback)



