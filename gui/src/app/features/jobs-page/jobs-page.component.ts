import {Component, OnDestroy, OnInit} from '@angular/core';
import {forkJoin} from 'rxjs';
import {tap} from 'rxjs/operators';
import {NzMessageService} from 'ng-zorro-antd/message';
import {HeaderTitle} from '../../core/domain/enums/header-title';
import {JobsServiceService} from '../../core/services/jobs-service.service';
import {ModelsService} from '../../core/services/models.service';
import {BaseScreenSettings} from './base-screen-settings';

@Component({
    selector: 'app-jobs-page',
    templateUrl: './jobs-page.component.html',
    styleUrls: ['./jobs-page.component.css']
})
export class JobsPageComponent extends BaseScreenSettings implements OnInit, OnDestroy {
    public readonly title: HeaderTitle = HeaderTitle.DISPLAY;
    public readonly PAGE_SIZE = 5;
    public downloadableModels: any;
    public jobsToDisplay: Array<string> = [];
    public allJobs: Array<string> = [];
    public pageIndex = 1;
    public finishedJobs: Array<string> = [];
    public logsModalSettings = {
        isVisible: false,
        specificLogsJobTitle: ''
    };
    public logs: Array<string> = [];
    private specificJob;
    private refreshInterval;

    constructor(private jobsService: JobsServiceService,
                private modelsService: ModelsService,
                private message: NzMessageService) {

        super();
    }


    ngOnInit(): void {
        this.jobsService.getAllJobs()
            .subscribe((allJobs) => {
                this.allJobs = allJobs;
                this.updatePage();
            }, (error) => this.message.error(error));

        this.initPage();
        this.refreshInterval = setInterval(this.initPage, 5000);
    }

    ngOnDestroy() {
        clearInterval(this.refreshInterval);
    }

    // function to manage pagination
    public moveToPage($event) {
        this.pageIndex = $event;
        this.updatePage();
    }

    // returns the logs list of a certain job
    public logsButton(jobs: string) {
        this.logsModalSettings.specificLogsJobTitle = jobs;
        this.specificJob = jobs;
        this.jobsService.logs({name: jobs})
            .subscribe((logs) => {
                this.logs = logs;
            }, (error) => {
                this.message.error(error);
                this.logsModalSettings.isVisible = false;
            });
        this.logsModalSettings.isVisible = true;
    }

    // deletes the selected value from the APIs list
    public onJobRemove(jobs: string) {
        const indexToRemove = this.allJobs.indexOf(jobs);
        this.allJobs.splice(indexToRemove, 1);
        this.updatePage();
        this.jobsService.killJob({name: jobs})
            .subscribe(() => {
            }, (e) => {
                this.allJobs.unshift(jobs);
                this.updatePage();
                this.message.error(e);
            });
    }

    // linked to the button inside the logs modal to update the logs list
    public handleRefreshMiddle(): void {
        this.jobsService.logs({name: this.specificJob})
            .subscribe((logs) => this.logs = logs,
                (error) => this.message.error(error));
    }

    private initPage = () => {
        return forkJoin([this.jobsService.getFinishedJobs()
            .pipe(tap((finishedJobs) => this.finishedJobs = finishedJobs)),
            this.modelsService.getDownloadableModels()
                .pipe(tap((models) => this.downloadableModels = models))
        ]).subscribe(() => this.updatePage(),
            (error) => this.message.error(error));
    }

    private updatePage() {
        this.jobsToDisplay = [...this.allJobs].splice
        ((this.pageIndex - 1) * this.PAGE_SIZE, this.PAGE_SIZE);
    }
}
