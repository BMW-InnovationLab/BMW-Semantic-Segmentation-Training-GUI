import {AdvancedHyperParameters} from './hyperparemeters';
import {GeneralSettingsConfig} from './general-settings-config';
import {WeightType} from '../enums/weight-type';

export class Config implements GeneralSettingsConfig, AdvancedHyperParameters{
    // hyper parameters
    lr: number = 0.010;
    batch_size: number = 1;
    validation_batch_size: number = 1;
    epochs: number = 15;
    momentum: number = 0.9;
    weight_decay: number = 0.0001;
    num_workers: number = 1;
    augment_data: boolean = true;
    crop_size: number = 480;
    base_size: number = 520;
    // from general settings
    model_name: string;
    gpus: number[];
    weight_type: WeightType = WeightType.PRE_TRAINED;
    backbone: string = 'resnet101';
    network: string = 'deeplab';
    base_weight_name: string = 'deeplab_resnet101';
    pretrained_dataset: string = 'voc';
    base_model_name: string = 'checkpoint_model';
}
