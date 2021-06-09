import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class InfrastructureService {
  private readonly baseUrl;

  constructor(private http: HttpClient) {
    const serviceUrl = environment.dockerSDKUrl;
    this.baseUrl = serviceUrl +  '/infrastructure';
  }

  getAvailableGPUs() {
    return this.http.get<any>(this.baseUrl + '/gpu/info');
  }

  getUsedPorts() {
    return this.http.get<string[]>(this.baseUrl + '/used/ports');
  }
}
