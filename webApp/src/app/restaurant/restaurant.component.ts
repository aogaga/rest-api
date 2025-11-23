import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RestaurantService } from '../services/restaurant/restaurant.service';
import { Restaurant } from '../models/restaurant/restaurant';

@Component({
  selector: 'app-restaurant',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './restaurant.component.html',
  styleUrls: ['./restaurant.component.scss'] // fixed typo
})
export class RestaurantComponent implements OnInit {
  title = 'Rest App';
  restaurants: Restaurant[] = [];
  error = '';
  loading = false; // default to false

  constructor(private restaurantService: RestaurantService) {
    this.loading = false;
  }

  ngOnInit(): void {
    this.loading = false;
  }

  search(term: string): void {
    if (!term.trim()) return;

    this.loading = true;
    this.error = '';
    this.restaurants = []; // clear previous results

    this.restaurantService.search(term).subscribe({
      next: (data: Restaurant[]) => {
        this.restaurants = data;
        this.loading = false;
        console.log('Restaurants:', data);
      },
      error: (err) => {
        console.error('Error fetching restaurants:', err);
        this.error = 'Failed to fetch restaurants';
        this.loading = false;
      }
    });
  }

  trackById(index: number, restaurant: Restaurant): string {
    return restaurant.id; // assuming each restaurant has a unique `id`
  }
}
