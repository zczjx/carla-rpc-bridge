import json
data = {
    "transform_0":{   
        "location":{
                "x":-2.8,
                "y":0.0,
                "z":4.6
        },
        "rotation":{
                "roll":0.0,
                "pitch":6.0,
                "yaw":0.0
        },
        "attachmentType":'SpringArmGhost'
    },
    "transform_1":{   
        "location":{
                "x":4.164,
                "y":0.0,
                "z":0.6
        },
        "rotation":{
                "roll":0.0,
                "pitch":12,
                "yaw":7
        },
        "attachmentType":'Rigid'
    },
    "transform_2":{   
        "location":{
                "x":2,
                "y":-0.1,
                "z":1.345
        },
        "rotation":{
                "roll":0,
                "pitch":0,
                "yaw":7
        },
        "attachmentType":'Rigid'
    },
    "transform_3":{   
        "location":{
                "x":2,
                "y":0.0425,
                "z":1.345
        },
        "rotation":{
                "roll":0,
                "pitch":0,
                "yaw":0
        },
        "attachmentType":'Rigid'
    },
    "transform_4":{   
        "location":{
                "x":2.13,
                "y":1.06,
                "z":1.03
        },
        "rotation":{
                "roll":0,
                "pitch":20,
                "yaw":-84
        },
        "attachmentType":'Rigid'
    },
    "transform_5":{   
        "location":{
                "x":-1.14,
                "y":0.055,
                "z":0.9
        },
        "rotation":{
                "roll":0,
                "pitch":10,
                "yaw":-180
        },
        "attachmentType":'Rigid'
    },
    "transform_6":{   
        "location":{
                "x":-2.12,
                "y":-1.05,
                "z":1.14
        },
        "rotation":{
                "roll":0,
                "pitch":0,
                "yaw":-150
        },
        "attachmentType":'Rigid'
    },
    "transform_7":{   
        "location":{
                "x":-2.1,
                "y":1.03,
                "z":1.14
        },
        "rotation":{
                "roll":0,
                "pitch":0,
                "yaw":150
        },
        "attachmentType":'Rigid'
    },
    "transform_8":{   
        "location":{
                "x":2.1,
                "y":1.04,
                "z":1.03
        },
        "rotation":{
                "roll":0,
                "pitch":20,
                "yaw":95
        },
        "attachmentType":'Rigid'
    }
}

with open ("transform_config.json", "w") as f:
    json.dump(data, f)

data_sensor = {
    "sensor0":{
        "bp_type":'sensor.camera.rgb',
        "colorconvert_type":'Raw',
        "cam_type":'Camera RGB',
        "attr_list":{}
    },
    "sensor1":{
        "bp_type":'sensor.camera.depth',
        "colorconvert_type":'Raw',
        "cam_type":'Camera Depth (Raw)',
        "attr_list":{}
    },
    "sensor2":{
        "bp_type":'sensor.camera.depth',
        "colorconvert_type":'Depth',
        "cam_type":'Camera Depth (Gray Scale)',
        "attr_list":{}
    },
    "sensor3":{
        "bp_type":'sensor.camera.depth',
        "colorconvert_type":'LogarithmicDepth',
        "cam_type":'Camera Depth (Logarithmic Gray Scale)',
        "attr_list":{}
    },
    "sensor4":{
        "bp_type":'sensor.camera.semantic_segmentation',
        "colorconvert_type":'Raw',
        "cam_type":'Camera Semantic Segmentation (Raw)',
        "attr_list":{}
    },
    "sensor5":{
        "bp_type":'sensor.camera.semantic_segmentation',
        "colorconvert_type":'CityScapesPalette',
        "cam_type":'Camera Semantic Segmentation (CityScapes Palette)',
        "attr_list":{}
    },
    "sensor6":{
        "bp_type":'sensor.camera.semantic_segmentation',
        "colorconvert_type":'CityScapesPalette',
        "cam_type":'Camera Instance Segmentation (CityScapes Palette)',
        "attr_list":{}
    },
    "sensor7":{
        "bp_type":'sensor.camera.semantic_segmentation',
        "colorconvert_type":'Raw',
        "cam_type":'Camera Instance Segmentation (Raw)',
        "attr_list":{}
    },
    "sensor8":{
        "bp_type":'sensor.lidar.ray_cast',
        "colorconvert_type":'None',
        "cam_type":'Lidar (Ray-Cast)',
        "attr_list":{'range': '50'}
    },
    "sensor9":{
        "bp_type":'sensor.camera.dvs',
        "colorconvert_type":'Raw',
        "cam_type":'Dynamic Vision Sensor',
        "attr_list":{}
    },
    "sensor10":{
        "bp_type":'sensor.camera.rgb',
        "colorconvert_type":'Raw',
        "cam_type":'Camera RGB Distorted',
        "attr_list":{
            'lens_circle_multiplier': '3.0',
            'lens_circle_falloff': '3.0',
            'chromatic_aberration_intensity': '0.5',
            'chromatic_aberration_offset': '0'
        }
    },
    "sensor11":{
        "bp_type":'sensor.camera.optical_flow',
        "colorconvert_type":'Raw',
        "cam_type":'Optical Flow',
        "attr_list":{}
    },
    "sensor12":{
        "bp_type":'sensor.camera.normals',
        "colorconvert_type":'Raw',
        "cam_type":'Camera Normals',
        "attr_list":{}
    }
}

with open("sensor_config.json", "w") as f1:
    json.dump(data_sensor, f1)