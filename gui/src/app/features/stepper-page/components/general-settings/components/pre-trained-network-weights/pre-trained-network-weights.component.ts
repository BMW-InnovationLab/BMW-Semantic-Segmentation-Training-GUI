import {Component, Input, ViewChild} from '@angular/core';
import {BaseStepperSubFormComponent} from '../../base-stepper-sub-form-component';
import {NzFormControlComponent} from 'ng-zorro-antd/form';
import {FormBuilder, Validators} from '@angular/forms';
import {Architecture} from '../../../../../../core/domain/models/architecture';

@Component({
    selector: 'app-pre-trained-network-weights',
    templateUrl: './pre-trained-network-weights.component.html',
    styleUrls: ['./pre-trained-network-weights.component.css']
})
export class PreTrainedNetworkWeightsComponent extends BaseStepperSubFormComponent {
    @Input() networks: Architecture;
    @ViewChild('formControlComponent') formControl: NzFormControlComponent;

    constructor(private fb: FormBuilder) {
        super();
        this.form = this.fb.group({
            network: ['', [Validators.required]]
        });
    }

    public getFields() {
        const fields = this.form.value.network.split('_');
        return {
            network: fields[0],
            backbone: fields[1],
            pretrained_dataset: fields[2]
        };
    }
}
