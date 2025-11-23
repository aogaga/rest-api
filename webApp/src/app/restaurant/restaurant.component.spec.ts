import { ComponentFixture, TestBed } from '@angular/core/testing';
import { of, throwError } from 'rxjs';
import { RestaurantComponent } from './restaurant.component';
import { RestaurantService } from '../services/restaurant/restaurant.service';
import { Restaurant } from '../models/restaurant/restaurant';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

describe('RestaurantComponent', () => {
  let component: RestaurantComponent;
  let fixture: ComponentFixture<RestaurantComponent>;
  let mockRestaurantService: jasmine.SpyObj<RestaurantService>;

  const dummyRestaurants: Restaurant[] = [
    {
      id: '1',
      name: 'Test Restaurant',
      address: '123 Main St',
      city: 'Cityville',
      rating: 4.5,
      phone: '123-456-7890',
      url: 'https://example.com',
      categories: ['Italian', 'Pizza']
    }
  ];

  beforeEach(async () => {
    mockRestaurantService = jasmine.createSpyObj('RestaurantService', ['search']);

    await TestBed.configureTestingModule({
      imports: [
        RestaurantComponent, // standalone component
        FormsModule,
        CommonModule
      ],
      providers: [
        { provide: RestaurantService, useValue: mockRestaurantService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(RestaurantComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the component', () => {
    expect(component).toBeTruthy();
  });

  it('should call restaurantService.search when search is called', () => {
    mockRestaurantService.search.and.returnValue(of(dummyRestaurants));

    component.search('pizza');

    expect(mockRestaurantService.search).toHaveBeenCalledWith('pizza');
  });

  it('should populate restaurants on successful search', () => {
    mockRestaurantService.search.and.returnValue(of(dummyRestaurants));

    component.search('pizza');

    expect(component.restaurants).toEqual(dummyRestaurants);
    expect(component.loading).toBeFalse();
    expect(component.error).toBe('');
  });

  it('should set error message on failed search', () => {
    const errorResponse = new Error('Network error');
    mockRestaurantService.search.and.returnValue(throwError(() => errorResponse));

    component.search('pizza');

    expect(component.restaurants).toEqual([]);
    expect(component.loading).toBeFalse();
    expect(component.error).toBe('Failed to fetch restaurants');
  });
});
