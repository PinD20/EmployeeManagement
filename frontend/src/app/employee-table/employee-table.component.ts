import { Component } from '@angular/core';
import { EmployeeService } from '../services/employee.service';
import { DepartmentService } from '../services/department.service';
import { FormGroup, FormBuilder, ReactiveFormsModule } from '@angular/forms';
import Swal from 'sweetalert2';

@Component({
  selector: 'app-employee-table',
  standalone: true,
  imports: [ReactiveFormsModule],
  templateUrl: './employee-table.component.html',
  styleUrl: './employee-table.component.css'
})
export class EmployeeTableComponent {

  employeesList: any = []; //Lista de empleados
  editEmployeeForm: FormGroup; //Formulario para editar empleado

  constructor(
    private employeeService: EmployeeService,
    private formBuilder: FormBuilder
  ) { 
    this.getEmployees();
    this.editEmployeeForm = this.formBuilder.group({
      codigo: [0],
      nombre: [''],
      apellido: [''],
      codigo_departamento: [0],
      departamento: [''],
      cargo: [''],
      fecha_contratacion: ['']
    });
  }

  //Obtener lista de empleados
  getEmployees() {
    this.employeeService.getEmployees()
    .subscribe(
      res => {
        let data:any = res;
        this.employeesList = data.employees;
      },
      err => {
        alert(err);
      }
    )
  }

  deleteEmployee(employee: any){
    Swal.fire({
      title: '¿Estás seguro?',
      text: `Se eliminará al empleado ${employee.nombre} ${employee.apellido}`,
      icon: "warning",
      showCancelButton: true,
      confirmButtonColor: "#3085d6",
      cancelButtonColor: "#d33",
      confirmButtonText: "Sí, continuar",
      cancelButtonText: "Cancelar"
    }).then((result) => {
      if (result.isConfirmed) {
        this.employeeService.deleteEmployee(employee.codigo)
        .subscribe(
          res => {
            //Actualiza la lista de empleados
            this.getEmployees();
            Swal.fire({
              title: "Empleado eliminado",
              text: "El empleado fue eliminado con éxito.",
              icon: "success"
            });
          },
          err => {
            console.log(err);
            Swal.fire({
              icon: "error",
              title: "Oops...",
              text: "Ocurrió un error durante la eliminación del empleado.",
            });
          }
        )
      }
    });
  }

  openEditModal(employee: any){
    //Setear valores del empleado en el formulario
    this.editEmployeeForm.setValue({
      codigo: employee.codigo,
      nombre: employee.nombre,
      apellido: employee.apellido,
      codigo_departamento: employee.codigo_departamento,
      departamento: employee.departamento,
      cargo: employee.cargo,
      fecha_contratacion: employee.fecha_contratacion
    });

    //Abrir formulario de edición
    const modal = new (window as any).bootstrap.Modal(document.getElementById('editEmployeeModal'));
    modal.show();
  }

  // Guardar cambios de edición
  onSubmitEdit() {
    if (this.editEmployeeForm.valid) {
      const editedEmployee = this.editEmployeeForm.value;
      this.employeeService.editEmployee(editedEmployee)
      .subscribe(
        res => {
          this.getEmployees(); //Actualizar lista de empleados
          alert("ok")
        },
        err => {
          alert(err);
        }
      )

      // Cerrar el modal después de guardar los cambios
      const modal = (window as any).bootstrap.Modal.getInstance(document.getElementById('editEmployeeModal'));
      modal.hide();
    }
  }
}
