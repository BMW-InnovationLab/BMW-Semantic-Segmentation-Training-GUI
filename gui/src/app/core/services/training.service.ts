import {Injectable} from '@angular/core';
import {environment} from '../../../environments/environment.prod';
import {HttpClient} from '@angular/common/http';
import {Observable, of} from 'rxjs';
import {tap} from 'rxjs/operators';
import {DatasetPreparationInput} from '../domain/models/dataset-preparation-input';


@Injectable({
    providedIn: 'root'
})
export class TrainingService {
    private readonly trainingUrl = environment.trainingUrl;

    constructor(private http: HttpClient) {
    }

    public prepareDataset(fullConfig: DatasetPreparationInput, port: number = 0): Observable<any> {
        const url = this.trainingUrl  + port + '/data_preparation';
        return this.http.post(url, fullConfig);
    }

    public isReachable(port: number): Observable<boolean> {
        const url = this.trainingUrl + port + '/health';
        return this.http.get<any>(url);
    }

    public train(fullConfig: DatasetPreparationInput, port: number): Observable<any> {
        const url = this.trainingUrl + port + '/training';
        return this.http.post(url, fullConfig);
    }
}
