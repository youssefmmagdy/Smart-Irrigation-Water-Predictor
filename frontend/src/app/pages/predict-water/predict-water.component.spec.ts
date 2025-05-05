import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PredictWaterComponent } from './predict-water.component';

describe('PredictWaterComponent', () => {
  let component: PredictWaterComponent;
  let fixture: ComponentFixture<PredictWaterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PredictWaterComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PredictWaterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
