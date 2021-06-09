import { Injectable } from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {DatasetInformation} from '../domain/models/dataset-information';


@Injectable({
  providedIn: 'root'
})
export class DatasetService {
  private readonly baseUrl;

  constructor(private http: HttpClient) {
    const serviceUrl = environment.dockerSDKUrl;
    this.baseUrl = serviceUrl + '/dataset';
  }

  public getDataSets() {
    return this.http.get<string[]>(this.baseUrl);
  }

  public validateDataset(datasetInformation: DatasetInformation) {
    return this.http.post<HttpResponse<any>>(this.baseUrl + '/validate', datasetInformation);
  }

  public getClasses(datasetInformation: DatasetInformation){
    return this.http.post<DatasetInformation>(this.baseUrl + '/classes', datasetInformation);
  }
}
