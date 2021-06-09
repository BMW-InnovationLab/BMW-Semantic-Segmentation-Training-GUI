import {Config} from './full-config';
import {DatasetInformation} from './dataset-information';

export interface DatasetPreparationInput {
    dataset_info: DatasetInformation;
    config: Config;
}
