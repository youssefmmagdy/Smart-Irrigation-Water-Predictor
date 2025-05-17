import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  {
    path: 'predict-water',
    loadComponent: () =>
      import('./pages/predict-water/predict-water.component').then(
        (m) => m.PredictWaterComponent
      ),
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}

export { routes }; // Export the routes constant