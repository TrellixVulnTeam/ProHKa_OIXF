import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map } from 'rxjs/operators';
import { getCookie } from 'src/app/shared/shared';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  readonly APIUrl = "http://127.0.0.1:8000/";
  constructor(private http: HttpClient) { }


  login(data: any): Observable<any> {
    let token = getCookie('csrftoken')
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'X-CSRFToken': token,
      })
    };
    return this.http.post<any>(this.APIUrl + "auth/api/login/", data, httpOptions).pipe(
      map(user => {
        if (user && user.token) {
          localStorage.setItem("currentUser", user.token)
        }
        return user;
      })
    );
  }


}
