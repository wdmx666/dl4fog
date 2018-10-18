"""
@Name:        preparation
@Description: Do some initialization
@Author:      Lucas Yu
@Created:     2018/9/13
@Copyright:   (c) GYENNO Science, Shenzhen, Guangdong 2018
@Licence:
"""


class HARConfig(object):
    DATADIR = r'E:\my_proj\fog_recognition\fog_optimization\dl4fog\resources\UCI HAR Dataset'
    SIGNALS = ["body_acc_x", "body_acc_y", "body_acc_z", "body_gyro_x", "body_gyro_y", "body_gyro_z", "total_acc_x",
               "total_acc_y", "total_acc_z"]

    @classmethod
    def dataSupplier(cls):
        from ..my_har.controllers import DataSupplier
        service = DataSupplier(dependencies='')
        service.set_para_with_prop({'DATADIR': cls.DATADIR, 'SIGNALS': cls.SIGNALS})
        return service

    @classmethod
    def APPipeline(cls):
        from ..commons.scheduler import MyScheduler
        pipe = MyScheduler()
        pipe.add_processor(cls.dataSupplier())
        return pipe