//// filepath: c:\Users\Yusuf\Documents\Bachelor\Code\frontend\Bachelor\src\app\api\api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  BACKEND_PORT_NUMBER = parseInt((<any>import.meta).env['BACKEND_PORT_Number'] || '8000', 10);
  private baseUrl = `http://localhost:${this.BACKEND_PORT_NUMBER}`; // Adjust the URL as needed

  constructor(private http: HttpClient) {}

  loadModel(modelId: string): Observable<any> {
    // Send a request to /load/{modelId} endpoint
    return this.http.post<any>(`${this.baseUrl}/load/${modelId}`, {});
  }

  predict(modelId: string, data: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/predict/${modelId}`, data);
  }
}