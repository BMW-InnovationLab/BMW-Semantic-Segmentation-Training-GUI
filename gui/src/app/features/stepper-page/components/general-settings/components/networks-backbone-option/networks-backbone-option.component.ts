import {Component, Input} from '@angular/core';
import {Architecture} from '../../../../../../core/domain/models/architecture';
import {BaseStepperSubFormComponent} from '../../base-stepper-sub-form-component';
import {FormBuilder, Validators} from '@angular/forms';

@Component({
    selector: 'app-networks-backbone-option',
    templateUrl: './networks-backbone-option.component.html',
    styleUrls: ['./networks-backbone-option.component.css']
})
export class NetworksBackboneOptionComponent extends BaseStepperSubFormComponent {
    @Input() architecture: Architecture;
    @Input() hideSettings = {backbone_hidden: false};

    constructor(private fb: FormBuilder) {
        super();
        this.form = this.fb.group({
            network: ['', [Validators.required]],
            backbone: [[], [Validators.required]],
        });
    }

    public getFields() {
        const values = this.form.value;
        return {
            network: values.network,
            backbone: values.backbone
        };
    }

    public isValid(): boolean {
        if (!this.hideSettings.backbone_hidden){
            return super.isValid();
        }
        this.form.controls.network.markAsDirty();
        this.form.controls.network.updateValueAndValidity();
        return this.form.controls.network.valid;
    }
}
