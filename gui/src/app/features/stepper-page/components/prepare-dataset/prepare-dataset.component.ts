import {Component, OnInit} from '@angular/core';
import {FormBuilder, Validators} from '@angular/forms';
import {NzMessageService} from 'ng-zorro-antd/message';
import {DatasetService} from '../../../../core/services/dataset.service';
import {BaseStepperSubFormComponent} from '../general-settings/base-stepper-sub-form-component';

@Component({
    selector: 'app-prepare-dataset',
    templateUrl: './prepare-dataset.component.html',
    styleUrls: ['./prepare-dataset.component.css']
})
export class PrepareDatasetComponent extends BaseStepperSubFormComponent implements OnInit {
    public datasets = [];

    constructor(private fb: FormBuilder,
                private datasetService: DatasetService,
                private message: NzMessageService) {
        super();
        this.form = this.fb.group({
            dataset_name: ['', [Validators.required]],
            training_ratio: [80, [Validators.required]],
            validation_ratio: [20, [Validators.required]]
        });
    }

    ngOnInit(): void {
        this.datasetService.getDataSets().subscribe((datasets: string[]) => {
                datasets.sort();
                this.datasets = datasets;
            },
            (error) => this.message.error(error));
    }

    public parserPercent = (value: string) => value.replace(/[.]\d*/, '');

    public changeTrainingRatio() {
        this.form.controls.validation_ratio.setValue(100 - this.form.value.training_ratio);
    }

    public getFields() {
        const formValues = this.form.value;
        return {
            dataset_name: formValues.dataset_name,
            train_ratio: formValues.training_ratio / 100
        };
    }
}
