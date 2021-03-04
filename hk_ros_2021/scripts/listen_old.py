#!/usr/bin/env python
import rospy 
import yaml
import rospkg
import tf
import tf_conversions
from apriltag_ros.msg import AprilTagDetectionArray 
from apriltag_ros.msg import Coordinates
from std_msgs.msg import String

rospy.init_node('listen', anonymous=True)

global transform
transform = tf.TransformListener()



class Object():
	
		def __init__(self, tag_id = None, obj_type = None, x_pos = None, y_pos = None):
					
				self.tag_id = tag_id
				self.obj_type = obj_type
				self.x_pos = x_pos
				self.y_pos = y_pos


def callback(data):
    
		if(len(data.detections) != 0):
				
				foundNew = True
				new_obj = Object()
				new_obj.obj_type = "A"
				new_obj.tag_id = data.detections[0].id[0]
				new_obj.x_pos = data.detections[0].pose.pose.pose.position.x
				new_obj.y_pos = data.detections[0].pose.pose.pose.position.y
	
				if len(object_list) == 0:
						object_list.append( {"obj_type": new_obj.obj_type, "XY_pos": [new_obj.x_pos,new_obj.y_pos], "tag_id": new_obj.tag_id} )

				for i in range(len(object_list)):
						
						if new_obj.tag_id == object_list[i]['tag_id']:
								foundNew = False
				
				if foundNew:
						
						object_list.append( {"obj_type": new_obj.obj_type, "XY_pos": [new_obj.x_pos,new_obj.y_pos], "tag_id": new_obj.tag_id} )

						transform.waitForTransform('/odom','/camera_rgb_optical_frame',rospy.Time(),rospy.Duration(1.0))
						(pos,rot) = transform.lookupTransform('/odom','/camera_rgb_optical_frame',rospy.Time())

						print(pos)
						

def listen():
		

		rospy.Subscriber("/tag_detections", AprilTagDetectionArray, callback)
		
		rospy.spin()

object_list = []

		
if __name__ == '__main__':
		listen()
		filename = "latest_output_file.yaml"
		filepath = rospkg.RosPack().get_path('hk_ros_2021') + '/exported_detection_logs/'

		with open(filepath + filename, 'w') as outfile:
				yaml.dump_all(object_list, outfile,explicit_start=True)
				print("DONE")
