import { Injectable } from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Observable} from 'rxjs';
import {Restaurant} from '../../models/restaurant/restaurant';

@Injectable({
  providedIn: 'root'
})
export class RestaurantService {

  private readonly baseUrl = environment.baseUrl;
  constructor(private http: HttpClient) { }

  search(term: string, limit: number = 10): Observable<Restaurant[]>{
    const url =`${this.baseUrl}?term=${term}&limit=${limit}`;
    return this.http.get<Restaurant[]>(url);
  }

}
