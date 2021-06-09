import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {GeneralSettingsComponent} from './components/general-settings/general-settings.component';
import {HyperParametersComponent} from './components/hyper-parameters/hyper-parameters.component';
import {ContainerSettings} from '../../core/domain/models/container-settings';
import {NzMessageService} from 'ng-zorro-antd/message';
import {Router} from '@angular/router';
import {forkJoin, throwError} from 'rxjs';
import {concatMap, switchMap, tap} from 'rxjs/operators';
import {HeaderTitle} from '../../core/domain/enums/header-title';
import {DatasetService} from '../../core/services/dataset.service';
import {DatasetInformation} from '../../core/domain/models/dataset-information';
import {BaseStepperSubFormComponent} from './components/general-settings/base-stepper-sub-form-component';
import {JobsServiceService} from '../../core/services/jobs-service.service';
import {ModelsService} from '../../core/services/models.service';
import {GeneralSettingsConfig} from '../../core/domain/models/general-settings-config';
import {TrainingService} from '../../core/services/training.service';
import {PrepareDatasetComponent} from './components/prepare-dataset/prepare-dataset.component';
import {retryWithDelay} from 'rxjs-boost/lib/operators';
import {DatasetPreparationInput} from '../../core/domain/models/dataset-preparation-input';

@Component({
    selector: 'app-stepper-page',
    templateUrl: './stepper-page.component.html',
    styleUrls: ['./stepper-page.component.css']
})
export class StepperPageComponent implements OnInit, OnDestroy {
    @ViewChild(PrepareDatasetComponent) prepareDataset: BaseStepperSubFormComponent;
    @ViewChild(GeneralSettingsComponent) generalSettings: BaseStepperSubFormComponent;
    @ViewChild(HyperParametersComponent) hyperParameters: BaseStepperSubFormComponent;
    public readonly title = HeaderTitle.CREATE;
    public currentStep = 0;
    public loadingSettings = {
        next: false,
        done: false,
        cancel: false,
        previous: false
    };
    public allJobs: Array<string> = [];
    public downloadableModels = [];
    public finishedJobs: Array<string> = [];
    public mobile: boolean;
    private containerSettings: ContainerSettings = new ContainerSettings();
    private generalSettingsConfig: GeneralSettingsConfig;
    private interval;
    private datasetInformation: DatasetInformation;

    constructor(private datasetService: DatasetService,
                private message: NzMessageService,
                private jobsService: JobsServiceService,
                private modelsService: ModelsService,
                private trainingService: TrainingService,
                private router: Router) {
    }

    ngOnInit(): void {
        this.initializeScreenSettings();
        this.getJobs();
        this.initPage();
        this.interval = setInterval(this.initPage, 5000);
    }

    ngOnDestroy() {
        clearInterval(this.interval);
    }

    public cancel(): void {
        this.jobsService.killJob(this.containerSettings)
            .subscribe(() => {
            }, (error) => this.message.error(error));
    }

    public pre(): void {
        this.currentStep -= 1;
        this.changeContent();
    }

    public next(): void {
        switch (this.currentStep) {
            case 0:
                if (this.prepareDataset.isValid()) {
                    const dataset_information: DatasetInformation = this.prepareDataset.getFields();
                    this.loadingSettings.next = true;
                    this.validateDataset(dataset_information);
                }
                break;
            case 1:
                if (this.generalSettings.isValid()) {
                    this.generalSettingsConfig = this.generalSettings.getFields();
                    this.loadingSettings.next = true;
                    this.startJob();
                }
        }
    }

    public done(): void {
        if (this.hyperParameters.isValid()) {
            const fullConfig: DatasetPreparationInput = {
                dataset_info: {...this.datasetInformation},
                config: {
                    ...this.generalSettingsConfig,
                    ...this.hyperParameters.getFields()
                }
            };
            this.loadingSettings.done = true;
            this.trainingService.prepareDataset(fullConfig, this.generalSettingsConfig.api_port)
                .pipe(concatMap(_ => this.trainingService.train(fullConfig, this.generalSettingsConfig.api_port)))
                .subscribe(() => {
                    this.router.navigate(['/jobs']);
                }, error => {
                    this.cancel();
                    this.router.navigate(['/jobs']).then(() => this.message.error(error));
                });
        }
    }

    private startJob() {
        const {model_name, api_port, gpus, ...rest} = this.generalSettingsConfig;
        this.containerSettings = {
            name: model_name,
            api_port,
            gpus,
            dataset_name: this.datasetInformation.dataset_name
        };

        const checkHealth = this.trainingService.isReachable(api_port)
            .pipe(retryWithDelay(5000, 4));

        let startSuccessful = false;
        this.jobsService.startNewJob(this.containerSettings)
            .pipe(tap(res => {
                if (!res.success) {
                    throwError('Could not start the container.');
                }
                startSuccessful = true;
                return res;
            })).pipe(switchMap(__ => checkHealth))
            .subscribe(_ => {
                this.loadingSettings.next = false;
                this.currentStep++;
                this.changeContent();
            }, error => {
                if (startSuccessful) {
                    this.cancel();
                }
                this.router.navigate(['/jobs']).then(() => this.message.error(error));
            });
    }


    private validateDataset(datasetInformation: DatasetInformation) {
        this.datasetService.validateDataset(datasetInformation)
            .pipe(tap((res: any) => {
                if (!res.success) {
                    throwError('Invalid dataset. Please choose another one.');
                }
            }))
            .pipe(switchMap((_) => this.datasetService.getClasses(datasetInformation)))
            .subscribe((classInformation: DatasetInformation) => {
                this.datasetInformation = classInformation;
                this.datasetInformation.train_ratio = datasetInformation.train_ratio;
                this.currentStep += 1;
                this.loadingSettings.next = false;
                this.changeContent();
            }, (error) => {
                this.loadingSettings.next = false;
                this.message.error(error);
            });
    }

    private initializeScreenSettings() {
        this.mobile = window.screen.width <= 768;
        window.onresize = () => {
            this.mobile = window.screen.width <= 768;
        };
    }

    private getJobs(): void {
        this.jobsService.getAllJobs()
            .subscribe((allJobs) => this.allJobs = allJobs,
                (error) => this.message.error(error));
    }

    private initPage = () => {
        return forkJoin([
            this.jobsService.getFinishedJobs()
                .pipe(tap((finishedJobs) => this.finishedJobs = finishedJobs)),
            this.modelsService.getDownloadableModels()
                .pipe(tap((models) => this.downloadableModels = models))
        ]).subscribe(() => {
        }, (error) => {
            this.message.error(error);
        });
    }

    // change content of each step
    private changeContent(): void {
        this.loadingSettings.previous = this.currentStep === 2;
    }
}
