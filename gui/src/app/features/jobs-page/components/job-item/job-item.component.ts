import {Component, EventEmitter, Input, Output} from '@angular/core';
import {environment} from '../../../../../environments/environment';
import {BaseScreenSettings} from '../../base-screen-settings';

@Component({
    selector: 'app-job-item',
    templateUrl: './job-item.component.html',
    styleUrls: ['./job-item.component.css']
})
export class JobItemComponent extends BaseScreenSettings {
    @Input() job: string;
    @Input() finishedJobs: Array<string> = [];
    @Input() downloadableModels: any = [];
    @Output() jobRemoved: EventEmitter<string> = new EventEmitter<string>();
    @Output() logsRequested: EventEmitter<string> = new EventEmitter<string>();
    public readonly modelsUrl = environment.dockerSDKUrl + '/models_services/';

    public removePopupText = 'Cancel Job?';

    // checks if the job is done or still running
    public jobIsDone = (job: string): number => {
        return this.finishedJobs && this.finishedJobs.indexOf(job);
    }

    // checks if job is running or done to state whether the popup text should be 'cancel job' or 'close job'
    public jobRemovePopupText(jobs) {
        if (this.jobIsDone(jobs) !== -1) {
            this.removePopupText = 'Close Job?';
        }
    }

    // gets the value of a model since the model is a dictionary list and is split into ModelKeys array and ModeValues array
    public getSpecificJobDownloadableModelURI = (job: string) => {
        if (this.downloadableModels !== undefined) {
            let value = '';
            Object.keys(this.downloadableModels).forEach(key => {
                if (job + '.zip' === key) {
                    value = this.downloadableModels[key];
                }
            });
            return value + encodeURIComponent('/' + job + '.zip');
        }
    }

    public onJobRemove(job) {
        this.jobRemoved.emit(job);
    }

    public logsButton(job: string) {
        this.logsRequested.emit(job);
    }
}
