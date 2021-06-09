export interface BasicHyperParameters{
    lr: number;
    batch_size: number;
    validation_batch_size: number;
    epochs: number;
}

export interface AdvancedHyperParameters extends BasicHyperParameters{
    momentum: number;
    weight_decay: number;
    num_workers: number;
    augment_data: boolean;
    crop_size: number;
    base_size: number;
}
