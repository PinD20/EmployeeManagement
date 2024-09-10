import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class EmployeeService {

  API: string = 'http://127.0.0.1:5000/'
  
  constructor(private http: HttpClient) { }

  getEmployees() {
    return this.http.get(`${this.API}/api/empleados`);
  }

  createEmployee(employee: any) {
    return this.http.post(`${this.API}/api/empleados`, employee);
  }

  editEmployee(employee: any) {
    return this.http.put(`${this.API}/api/empleados/${employee.codigo}`, employee);
  }

  deleteEmployee(employeeCode: any) {
    return this.http.delete(`${this.API}/api/empleados/${employeeCode}`);
  }
}
