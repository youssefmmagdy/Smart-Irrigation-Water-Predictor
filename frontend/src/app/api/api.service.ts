//// filepath: c:\Users\Yusuf\Documents\Bachelor\Code\frontend\Bachelor\src\app\api\api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  
  private baseUrl ='https://smart-irrigation-water-predictor.onrender.com';

  constructor(private http: HttpClient) {}

  loadModel(modelId: string): Observable<any> {
    // Send a request to /load/{modelId} endpoint
    return this.http.post<any>(`${this.baseUrl}/load/${modelId}`, {});
  }

  predict(modelId: string, data: any): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/predict/${modelId}`, data);
  }

  askOllama(question: string): Observable<any> {
    return this.http.post<any>(`${this.baseUrl}/ask-ollama`, { question });
  }
}