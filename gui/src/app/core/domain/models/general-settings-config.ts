export interface GeneralSettingsConfig {
    model_name: string;
    gpus: number[];
    weight_type: string;
    backbone?: string;
    network?: string;
    base_weight_name?: string;
    pretrained_dataset?: string;
    base_model_name?: string;
    api_port?: number;
}
