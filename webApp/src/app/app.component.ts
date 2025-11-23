import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {RestaurantComponent} from './restaurant/restaurant.component';
import {CommonModule} from '@angular/common';
import { HttpClientModule } from '@angular/common/http';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RestaurantComponent, CommonModule, HttpClientModule],
  templateUrl: './app.component.html',
  standalone: true,
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'Rest App';
}
