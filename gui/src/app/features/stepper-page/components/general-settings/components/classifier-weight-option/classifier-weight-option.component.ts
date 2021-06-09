import {Component, Input, ViewChild} from '@angular/core';
import {Architecture} from '../../../../../../core/domain/models/architecture';
import {NetworksBackboneOptionComponent} from '../networks-backbone-option/networks-backbone-option.component';
import {BaseStepperSubFormComponent} from '../../base-stepper-sub-form-component';

@Component({
    selector: 'app-classifier-weight-option',
    templateUrl: './classifier-weight-option.component.html',
    styleUrls: ['./classifier-weight-option.component.css']
})
export class ClassifierWeightOptionComponent extends BaseStepperSubFormComponent {
    @ViewChild(NetworksBackboneOptionComponent) networkOption: BaseStepperSubFormComponent;
    @ViewChild('classifierOption') classifierTreeSelect: BaseStepperSubFormComponent;
    @Input() architecture: Architecture;
    @Input() classifiers: Record<string, string>;
    public hideSettings = {backbone_hidden: true};

    constructor() {
        super();
    }

    public getFields() {
        const classifierFields = this.classifierTreeSelect.getFields();
        return {
            ...this.networkOption.getFields(),
            backbone: classifierFields.base_weight_name,
            base_model_name: classifierFields.base_model_name
        };
    }

    public isValid(): boolean {
        const networkValid = this.networkOption.isValid();
        const classifierValid = this.classifierTreeSelect.isValid();
        return networkValid && classifierValid;
    }
}
