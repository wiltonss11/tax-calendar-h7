import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { State } from '../models/state.model';
import { ObligationsResponse } from '../models/obligation.model';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

  getHealth(): Observable<any> {
    return this.http.get(`${this.baseUrl}/health`);
  }

  getStates(): Observable<State[]> {
    return this.http.get<State[]>(`${this.baseUrl}/states`);
  }

  getCounties(stateCode: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/counties/${stateCode}`);
  }

  getCities(stateCode: string, countyName: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/cities/${stateCode}/${encodeURIComponent(countyName)}`);
  }

  getObligations(filters?: {
    state?: string;
    county?: string;
    city?: string;
    date_range?: string;
  }): Observable<ObligationsResponse> {
    let params = new HttpParams();
    
    if (filters) {
      if (filters.state) params = params.set('state', filters.state);
      if (filters.county) params = params.set('county', filters.county);
      if (filters.city) params = params.set('city', filters.city);
      if (filters.date_range) params = params.set('date_range', filters.date_range);
    }

    return this.http.get<ObligationsResponse>(`${this.baseUrl}/calendar`, { params });
  }
}
