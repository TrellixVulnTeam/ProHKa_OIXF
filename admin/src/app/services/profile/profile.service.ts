import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ProfileInt } from 'src/app/components/profile/profileInterfa';

@Injectable({
  providedIn: 'root'
})
export class ProfileService {

  readonly APIUrl = "http://127.0.0.1:8000/";
  constructor(private http: HttpClient) { }

  getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2)
      return parts.pop().split(";").shift();
  }

  // ******************************* fetch all profile and and clientUser  *******************************
  getProfile(): Observable<any> {
    return this.http.get<ProfileInt>(this.APIUrl + "custom/api/show-profile/")
  }

  getClientUser(): Observable<any> {
    return this.http.get<any>(this.APIUrl + "auth/api/get-all-user/")
  }

  // ******************************* register profile **********************************
  registerProfile(data: ProfileInt): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': this.getCookie('csrftoken'),
      })
    };
    return this.http.post<ProfileInt>(this.APIUrl + "custom/api/show-profile/", data, httpOptions)
  }


  // *************************** retrieve command and message *******************************************
  getAllCommand(): Observable<any> {
    return this.http.get<any>(this.APIUrl + "custom/api/get-all-command/")
  }

  getAllMessage(): Observable<any> {
    return this.http.get<any>(this.APIUrl + "custom/api/retrieve-message/")
  }

  // ********************************** send status of command and message *******************************************
  sendStatus(id: number, data: string): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': this.getCookie('csrftoken'),
      })
    };
    return this.http.put<string>(this.APIUrl + "custom/api/edit-status-command/" + id + "/", { 'status': data }, httpOptions)
  }

  sendStatusMessage(id: number, data: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': this.getCookie('csrftoken'),
      })
    };
    return this.http.put<string>(this.APIUrl + "custom/api/edit-message/" + id + "/", { 'data': data }, httpOptions)
  }

  // ******************************************** ATTRIBUTE A OWNER TO A PROFILE ******************************
  setOwner(id: number, data: string) {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': this.getCookie('csrftoken'),
      })
    };
    return this.http.put<string>(this.APIUrl + "custom/api/edit-profile/" + id + "/", { 'data': data }, httpOptions)
  }


  // ****************************** DELETE DEMANDE MESSAGE AND PROFILE ******************************************
  deleteCommand(id: number): Observable<any> {
    return this.http.delete(this.APIUrl + "custom/api/edit-status-command/" + id + "/")
  }

  deleteMessage(id: number): Observable<any> {
    return this.http.delete(this.APIUrl + "custom/api/edit-message/" + id + "/")
  }

  deleteProfile(id: number): Observable<any> {
    return this.http.delete(this.APIUrl + "custom/api/edit-profile/" + id + "/")
  }


  // ********************************** send proposition profile to the client *******************************************
  proposition(data: {}): Observable<any> {
    const httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': this.getCookie('csrftoken'),
      })
    };
    return this.http.post<string>(this.APIUrl + "custom/api/send-proposition/", data, httpOptions)
  }

}
