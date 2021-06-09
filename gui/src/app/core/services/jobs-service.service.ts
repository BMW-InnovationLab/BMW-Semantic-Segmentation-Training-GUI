import {Injectable} from '@angular/core';
import {environment} from '../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {ContainerSettings} from '../domain/models/container-settings';
import {Observable} from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class JobsServiceService {
    private readonly baseUrl;

    constructor(private http: HttpClient) {
        const serviceUrl = environment.dockerSDKUrl;
        this.baseUrl = serviceUrl + '/jobs';
    }

    public getAllJobs() {
        return this.http.get<string[]>(this.baseUrl);
    }

    public startNewJob(json: ContainerSettings): Observable<any> {
        return this.http.post<any>(this.baseUrl + '/start', JSON.stringify(json));
    }

    public killJob(json: ContainerSettings): Observable<any> {
        return this.http.post<any>(this.baseUrl + '/stop', JSON.stringify(json));
    }

    public logs(json: ContainerSettings) {
        const postPath = '/container/logs';
        return this.http.post<string[]>(this.baseUrl + postPath, JSON.stringify(json));
    }

    public getFinishedJobs() {
        const postPath = '/container/finished';
        return this.http.get<string[]>(this.baseUrl + postPath);
    }
}
