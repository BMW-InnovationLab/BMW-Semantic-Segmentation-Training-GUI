import {ChangeDetectionStrategy, Component, Input, OnInit, ViewChild} from '@angular/core';
import {FormBuilder, FormControl, ValidationErrors, Validators} from '@angular/forms';
import {forkJoin, Observable, Observer} from 'rxjs';
import {NzMessageService} from 'ng-zorro-antd/message';
import {ModelsService} from '../../../../core/services/models.service';
import {JobsServiceService} from '../../../../core/services/jobs-service.service';
import {GpuInfo} from '../../../../core/domain/models/gpu-info';
import {InfrastructureService} from '../../../../core/services/infrastructure.service';
import {tap} from 'rxjs/operators';
import {WeightType} from '../../../../core/domain/enums/weight-type';
import {Architecture} from '../../../../core/domain/models/architecture';
import {BaseStepperSubFormComponent} from './base-stepper-sub-form-component';
import {NetworksBackboneOptionComponent} from './components/networks-backbone-option/networks-backbone-option.component';
import {PreTrainedNetworkWeightsComponent} from './components/pre-trained-network-weights/pre-trained-network-weights.component';
import {PreTrainedOfflineAndCheckpointOptionComponent} from './components/pre-trained-offline-and-checkpoint-option.component/pre-trained-offline-and-checkpoint-option.component';
import {ClassifierWeightOptionComponent} from './components/classifier-weight-option/classifier-weight-option.component';
import {GeneralSettingsConfig} from '../../../../core/domain/models/general-settings-config';


@Component({
    selector: 'app-general-settings',
    templateUrl: './general-settings.component.html',
    styleUrls: ['./general-settings.component.css'],
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class GeneralSettingsComponent extends BaseStepperSubFormComponent implements OnInit {
    @ViewChild('networkBackboneOption', {static: false}) networkBackBoneFields: NetworksBackboneOptionComponent;
    @ViewChild(PreTrainedNetworkWeightsComponent, {static: false}) pretrainedField: PreTrainedNetworkWeightsComponent;
    @ViewChild('checkpointTreeSelect', {static: false}) checkpointTreeSelectFields:
        PreTrainedOfflineAndCheckpointOptionComponent;
    @ViewChild('classifierWeightOptionComponent', {static: false}) classifierField: ClassifierWeightOptionComponent;

    @Input() downloadableModels: any;
    // tslint:disable-next-line:no-input-rename
    @Input('allJobs') runningJobs: Array<string> = [];
    public availableGPUs: Array<GpuInfo> = [];
    public disableSelection = false;
    public checkpoints: Array<string> = [];
    public weightTypeTooltip = 'Choose the desired training method';
    public architecture: Architecture = {} as Architecture;
    public preTrainedNetworksArchitecture: Architecture = {} as Architecture;
    public classifiers: Record<string, string> = {};
    public disableFormClick = false;

    constructor(private fb: FormBuilder,
                private infrastructureService: InfrastructureService,
                private jobsService: JobsServiceService,
                private modelsService: ModelsService,
                private message: NzMessageService) {
        super();
        this.form = this.fb.group({
            name: ['', [Validators.required], [this.userNameAsyncValidator]],
            gpus_count: [[], [Validators.required]],
            api_port: [0, [Validators.required]],
            weight_type: ['', Validators.required],
        });
    }

    private static getRandomPort(): string {
        return (Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000).toString();
    }

    public weightTypes = () => {
        return [
            {name: 'From scratch', value: WeightType.FROM_SCRATCH, field: this.networkBackBoneFields},
            {name: 'Transfer learning from online weights', value: WeightType.PRE_TRAINED, field: this.pretrainedField},
            {
                name: 'Transfer learning from local weights',
                value: WeightType.PRE_TRAINED_OFFILE,
                field: this.checkpointTreeSelectFields
            },
            {name: 'From checkpoint', value: WeightType.FROM_CHECKPOINT, field: this.checkpointTreeSelectFields},
            {
                name: 'Using classifier’s (Backbone) local weights ',
                value: WeightType.PRE_TRAINED_CLASSIFIER,
                field: this.classifierField
            }
        ];
    }

    ngOnInit(): void {
        this.initPage();
    }

    public excludedCharacters(val) {
        this.form.get('name').setAsyncValidators(this.userNameAsyncValidator);
        if (/[/\\^\[\]|`%]/.test(val.key)) {
            val.preventDefault();
        }
    }

    public userNameAsyncValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            const value = control.value.trim();
            const modelFound = Object.keys(this.downloadableModels).find(model => value === model.slice(0, -4));
            const jobFound = this.runningJobs.find(job => value === job);
            if (modelFound || jobFound) {
                observer.next({error: true, duplicated: true});
            } else {
                this.form.get('name').clearAsyncValidators();
                observer.next(null);
            }
            observer.complete();
        })

    public onNoGPUSelect(chosenArchitectures) {
        if (chosenArchitectures.includes('-1') && chosenArchitectures.length > 1) {
            this.disableSelection = true;
            this.form.controls.gpus_count.setValue(['-1']);
        } else {
            this.disableSelection = !!chosenArchitectures.includes('-1');
        }
    }

    public getFields() {
        let fields: GeneralSettingsConfig;
        const formValues = this.form.value;

        fields = {
            model_name: formValues.name.trim(),
            gpus: formValues.gpus_count.map(gpu => Number(gpu)),
            weight_type: formValues.weight_type,
            api_port: formValues.api_port,
            ...this.getComponentUsedForWeight().getFields()
        };
        return fields;
    }

    public isValid(): boolean {
        const generalSettingsValid = super.isValid();
        const weightsValid = this.getComponentUsedForWeight().isValid();
        return generalSettingsValid && weightsValid;
    }

    private getComponentUsedForWeight(): BaseStepperSubFormComponent {
        const formValues = this.form.value;
        const fieldsUsedForWeight = this.weightTypes()
            .find(withField => withField.value === formValues.weight_type);
        return fieldsUsedForWeight.field;
    }

    private initPage = () => {
        return forkJoin([
            this.infrastructureService.getAvailableGPUs()
                .pipe(tap((availableGPUs: Record<string, string>) => {
                    for (const [id, gpu] of Object.entries(availableGPUs)) {
                        if (id !== '-1') {
                            this.availableGPUs.push({
                                id,
                                info: gpu
                            });
                        }
                    }
                })),
            this.infrastructureService.getUsedPorts()
                .pipe(tap((usedPorts) => {
                    let randomPort;
                    do {
                        randomPort = GeneralSettingsComponent.getRandomPort();
                    } while (usedPorts.indexOf(randomPort) >= 0);
                    this.form.controls.api_port.setValue(Number(randomPort));
                })),
            this.modelsService.getCheckpoints()
                .pipe(tap((checkpoints) => this.checkpoints = checkpoints)),
            this.modelsService.getArchitecture()
                .pipe(tap((architecture) => this.architecture = architecture)),
            this.modelsService.getArchitecturePreTrained()
                .pipe(tap((preTrainedNetworksArchitecture) => this.preTrainedNetworksArchitecture = preTrainedNetworksArchitecture)),
            this.modelsService.getClassifiers()
                .pipe(tap((classifiers) => this.classifiers = classifiers))
        ]).subscribe(() => {
        }, (e) => this.message.error(e));
    }
}
