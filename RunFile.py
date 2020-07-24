# -*- coding: utf-8 -*-
"""
Created on Thu May 14 19:52:53 2020

@authors: caldeiral & youpele
"""

import tensorflow as tf 
tf.compat.v1.enable_eager_execution()
print(tf.reduce_sum(tf.random.normal([1000, 1000])))



class RunFile:
    '''
    This is python in-IDE as oppose to running DeepMedic
    software in the terminal. 
    Refer to DeepMedic github page for documentations.
    
    https://github.com/deepmedic/deepmedic#12-installation
    '''
    def deepmedic_train(model_path, train_path,
                        deepMedicRun_path = "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun",
                        wdir='C:/Users/michaely/Documents/deepmedic-master/deepmedic-master',
                        gpu = '-dev cuda0'):
        '''
        Training a model
        

        Parameters
        ----------
        model_path : String
            Path to the model.
        train_path : String
            Path to the train Config file.
        deepMedicRun_path : String, optional
            Path to the deepMedicRun file. The default is "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun".
        wdir : String, optional
            Path to the deepmedic-master folder. The default is 'C:/Users/michaely/Documents/deepmedic-master/deepmedic-master'.
        gpu : String, optional
            GPU. The default is '-dev cuda0'.

        Returns
        -------
        None.

        '''
    
        model = '-model ' + model_path
        train = '-train ' + train_path
        args = model + ' ' + train + ' ' + gpu
        args = args.replace('\\', "/")
        
        runfile(deepMedicRun_path, 
            args = args,
            wdir= wdir)
        
    def deepmedic_test(model_path, test_path, model_ckpt_path,
                       deepMedicRun_path = "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun",
                       wdir='C:/Users/michaely/Documents/deepmedic-master/deepmedic-master',
                       gpu = '-dev cuda0'):
        '''
        Testing a trained model.

        Parameters
        ----------
        model_path : String
            Path to the model.
        test_path : String
            Path to the testConfig file.
        model_ckpt_path : String
            Path to the model.ckpt file. 
        deepMedicRun_path : String, optional
            Path to the deepMedicRun file. The default is "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun".
        wdir : String, optional
            Path to the deepmedic-master folder. The default is 'C:/Users/michaely/Documents/deepmedic-master/deepmedic-master'.
        gpu : TYPE, optional
            GPU. The default is '-dev cuda0'.

        Returns
        -------
        None.

        '''
        
        
        
        model = '-model ' + model_path
        test = '-test ' + test_path
        load = '-load ' + model_ckpt_path
        args = model + ' ' + test + ' ' + load + ' ' +gpu
        args = args.replace('\\', "/")
        
        runfile(deepMedicRun_path,
                args = args,
                wdir= wdir)
        
    def deepmedic_resumeTraining(model_path, train_path, model_ckpt_path, 
                                   deepMedicRun_path = "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun",
                                   wdir='C:/Users/michaely/Documents/deepmedic-master/deepmedic-master',
                                   gpu = '-dev cuda0'):
        """
        Resuming an Interrupted Training Session



        Parameters
        ----------
        model_path : String
            Path to the model.
        train_path : String
            Path to the train Config file.
        model_ckpt_path : TYPE
            Path to the model.ckpt saved file from which training will resume.
        deepMedicRun_path : String, optional
            Path to the deepMedicRun file. The default is "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun".
        wdir : String, optional
            Path to the deepmedic-master folder. The default is 'C:/Users/michaely/Documents/deepmedic-master/deepmedic-master'.
        gpu : TYPE, optional
            GPU. The default is '-dev cuda0'.

        Returns
        -------
        None.

        """
        
        model = '-model ' + model_path
        train = '-train ' + train_path
        load = '-load ' + model_ckpt_path
        args = model + ' ' + train + ' ' + load + ' ' +gpu
        args = args.replace('\\', "/")
        
        runfile(deepMedicRun_path,
                args = args,
                wdir= wdir)
        
        
        
        
        
        
        
    def deepmedic_fineTuning (model_path, train_path, model_ckpt_path, 
                              deepMedicRun_path = "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun",
                              wdir='C:/Users/michaely/Documents/deepmedic-master/deepmedic-master',
                              gpu = '-dev cuda0' ):
        '''
        Fine tuning.

        Parameters
        ----------
        model_path : String
            Path to the model.
        train_path : String
            Path to the train Config file.
        model_ckpt_path : String
            Path to the model.ckpt file.
        deepMedicRun_path : String, optional
            Path to the deepMedicRun file.. The default is "C:/Users/michaely/Documents/deepmedic-master/deepmedic-master/deepMedicRun".
        wdir : String, optional
            Path to the deepmedic-master folder. The default is 'C:/Users/michaely/Documents/deepmedic-master/deepmedic-master'.
        gpu : String, optional
            GPU. The default is '-dev cuda0'.

        Returns
        -------
        None.

        '''
        
        transferLearning = '-resetopt'
        model = '-model ' + model_path
        train = '-train ' + train_path
        load = '-load ' + model_ckpt_path
        args = model + ' ' + train + ' ' + load + ' ' + transferLearning + ' ' + gpu
        args = args.replace('\\', "/")
        
        runfile(deepMedicRun_path,
                args = args,
                wdir= wdir)
        
        
        
        
        
        
        
        
        
        
        
# ./deepMedicRun -model ./examples/configFiles/deepMedic/model/modelConfig.cfg \
#                -train ./examples/configFiles/deepMedic/train/trainConfigForRefinement.cfg \
#                -load ./path/to/pretrained/network/filename.DATE+TIME.model.ckpt \
#                -resetopt \
#                -dev cuda0
