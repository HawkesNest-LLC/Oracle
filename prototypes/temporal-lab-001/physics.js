'use strict';
/** Idealized inertial twin comparison: Earth observer coordinate time, traveler proper time. */
const C=299792458;
function calculate(beta, earthYears){
  if(!Number.isFinite(beta)||beta<0||beta>=1)throw new RangeError('Speed fraction must be 0 <= beta < 1');
  if(!Number.isFinite(earthYears)||earthYears<0)throw new RangeError('Earth time must be nonnegative');
  const gamma=1/Math.sqrt((1-beta)*(1+beta));
  const travelerYears=earthYears/gamma;
  return {beta, speedMetersPerSecond:beta*C, gamma, earthYears, travelerYears, differenceYears:earthYears-travelerYears};
}
if(typeof module!=='undefined')module.exports={calculate,C};
