import { TestBed } from '@angular/core/testing';
import { RestaurantService } from './restaurant.service';
import { provideHttpClientTesting } from '@angular/common/http';
import { HttpTestingController } from '@angular/common/http/testing';

describe('RestaurantService', () => {
  let service: RestaurantService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        RestaurantService,
        provideHttpClientTesting() // <-- provides HttpClient for tests
      ]
    });

    service = TestBed.inject(RestaurantService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
