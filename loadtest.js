import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 },  // Ramp-up leve: sobe para 10 usuários virtuais
    { duration: '30s', target: 50 },   // Spike: sobe agressivamente para 50 usuários
    { duration: '30s', target: 50 },   // Mantém o estresse para dar tempo do HPA agir e os pods subirem
    { duration: '30s', target: 0 },   // Ramp-down: zera os usuários
  ],
};

export default function () {
  // Substitua pela URL gerada pela Route no OpenShift
  const url = 'http://demo-autoscale-route-default.apps.p1343.cecc.ihost.com/load';
  
  const res = http.get(url);
  
  // Pausa de meio segundo entre as requisições de cada usuário virtual
  sleep(0.5); 
}