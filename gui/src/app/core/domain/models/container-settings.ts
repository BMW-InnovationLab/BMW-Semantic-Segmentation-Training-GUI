export class ContainerSettings {
    name: string;
    dataset_name?: string;
    api_port?: number;
    gpus?: number[];

    constructor();
    constructor(name?: string, api_port?: number, gpus_count?: number[]) {
        this.name = name || '';
        this.api_port = api_port || 0;
        this.gpus = gpus_count || [];
        this.dataset_name = '';
    }
}
