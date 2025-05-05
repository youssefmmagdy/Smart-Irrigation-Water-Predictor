import { Routes } from '@angular/router';
import { PredictWaterComponent } from './pages/predict-water/predict-water.component';

export const routes: Routes = [
  { path: '', redirectTo: 'predict', pathMatch: 'full' },
  { path: 'predict', component: PredictWaterComponent }
];
