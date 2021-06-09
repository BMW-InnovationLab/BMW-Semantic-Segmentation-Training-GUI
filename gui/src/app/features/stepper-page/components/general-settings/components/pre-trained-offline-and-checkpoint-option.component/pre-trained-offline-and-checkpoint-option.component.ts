import {ChangeDetectionStrategy, Component, Input, OnChanges, OnInit, SimpleChanges} from '@angular/core';
import {BaseStepperSubFormComponent} from '../../base-stepper-sub-form-component';
import {FormBuilder, Validators} from '@angular/forms';
import {NzTreeNode} from 'ng-zorro-antd/tree';

@Component({
    selector: 'app-pre-trained-offline-and-checkpoint-option',
    templateUrl: './pre-trained-offline-and-checkpoint-option.component.html',
    styleUrls: ['./pre-trained-offline-and-checkpoint-option.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class PreTrainedOfflineAndCheckpointOptionComponent extends BaseStepperSubFormComponent implements OnInit, OnChanges {
    @Input() localWeights: any = {};
    public localWeightsNodes: any;

    constructor(private fb: FormBuilder) {
        super();
        this.localWeightsNodes = [];
        this.form = this.fb.group({
            chosenWeight: ['', [Validators.required]]
        });
    }

    ngOnInit(): void {
       this.formatWeights();
    }

    ngOnChanges(changes: SimpleChanges) {
        this.formatWeights();
    }

    private formatWeights() {
        this.localWeightsNodes = [];
        const formattedWeights: Record<string, string[]> = {};
        Object.values(this.localWeights).forEach((value: string) => {
            formattedWeights[value] = Object.keys(this.localWeights)
                .filter(key => this.localWeights[key] === value);
        });
        for (const [netName, models] of Object.entries(formattedWeights)) {
            const children = [];
            models.forEach(model => children.push({
                title: model,
                key: model + '|' + this.localWeights[model],
                isLeaf: true
            }));
            this.localWeightsNodes.push({
                title: netName,
                key: netName,
                children,
                selectable: false
            });
        }
    }

    public getFields() {
        const modelWeightPair: string[] = this.form.value.chosenWeight.split('|');
        return {
            base_model_name: modelWeightPair[0],
            base_weight_name: modelWeightPair[1]
        };
    }

    public showValue(node: NzTreeNode) {
        return node.key.split('|').join(' | ');
    }
}
