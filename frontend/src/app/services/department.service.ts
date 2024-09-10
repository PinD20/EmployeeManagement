import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DepartmentService {

  API: string = 'http://127.0.0.1:5000/'
  
  constructor(private http: HttpClient) { }

  getEmployees() {
    return this.http.get(`${this.API}/api/departamentos`);
  }

}
