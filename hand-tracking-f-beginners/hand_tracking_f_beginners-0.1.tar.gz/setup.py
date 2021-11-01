from distutils.core import setup
setup(
  name = 'hand_tracking_f_beginners',         
  packages = ['hand_tracking_f_beginners'],   
  version = '0.1',      
  license='MIT',        
  description = 'I have created a python project for hand tracking for absolute beginners. I am to a beginner too. I found that on internet it is hard get the perfect code and to start up with computer vision and it is just a littlie fun project',   
  author = 'Aayush',                   
  author_email = 'aayushbannapure6@gmail.com',      
  url = 'https://github.com/AayushBannapure/hand_Tracking_For_beginners',   
  download_url = 'https://github.com/AayushBannapure/hand_Tracking_For_beginners/archive/refs/tags/hand_tracking_f_beginners.tar.gz',    
  keywords = ['Hand_Tracking', 'Hand_Tracking_f_beginners', 'Hand_tracking_for_beginners'],  
  install_requires=[            
          'mediapipe',
          'keyboard',
          'time',
          'opencv-python'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',  
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)