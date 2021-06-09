import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';
import {of} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ModelsService {
  private readonly baseUrl;

  constructor(private http: HttpClient) {
    const serviceUrl = environment.dockerSDKUrl;
    this.baseUrl = serviceUrl + '/models';
  }

  getDownloadableModels() {
    return this.http.get<any>(this.baseUrl + '/downloadable');
  }

  getArchitecture(){
    return this.http.get<any>(this.baseUrl + '/architecture');
  }

  getArchitecturePreTrained(){
    return this.http.get<any>(this.baseUrl + '/architecture/pretrained_networks');
  }

  getCheckpoints(){
    return this.http.get<any>(this.baseUrl + '/checkpoints');
  }

  getClassifiers(){
    return this.http.get<any>(this.baseUrl + '/classifiers');
  }
}
