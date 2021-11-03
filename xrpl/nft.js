// XLS-14d Sample implementation

const xrplValueToNft = value => {
    const data = String(Number(value)).split(/e/i)
  
    const finish = returnValue => {
      const unsignedReturnValue = returnValue.replace(/^\-/, '')
      if (unsignedReturnValue.length > 83) {
        // Too many tokens to be NFT-like as per XLS14d proposal
        return false
      }
      if (data.length > 1 && unsignedReturnValue.slice(0, 2) === '0.' && Number(data[1]) < -70) {
        // Positive below zero amount, could be NFT
        return (sign === '-' ? -1 : 1) * Number(
          (unsignedReturnValue.slice(2) + '0'.repeat(83 - unsignedReturnValue.length))
            .replace(/^0+/, '')
        )
      }
      return false
    }
  
    if (data.length === 1) {
      // Regular (non-exponent)
      return false
    }
  
    let z = ''
    const sign = value < 0 ? '-' : ''
    let str = data[0].replace('.', '')
    let mag = Number(data[1]) + 1
  
    if (mag < 0) {
      z = sign + '0.'
      while (mag++) {
        z += '0'
      }
      return finish(z + str.replace(/^\-/, ''))
    }
    mag -= str.length
  
    while (mag--) {
      z += '0'
    }
    return finish(str + z)
  }
  
  const nftValuetoXrpl = (value, accountBalance) => {
    const unsignedValue = String(value).replace(/^-/, '')
    const sign = unsignedValue.length < String(value).length ? '-' : ''

    // accountBalance: xrpl string notation, optional, if intention to force NFT check
    if (typeof accountBalance !== 'undefined' && xrplValueToNft(accountBalance) === false) {
      throw new Error('Source balance is not NFT-like')
    }
    if (!unsignedValue.match(/^[0-9]+$/)) {
      throw new Error('Only non-float & non-scientific notation values accepted')
    }
    
    return sign + '0.' + '0'.repeat(81 - unsignedValue.length) + unsignedValue
  }
  
  console.log(xrplValueToNft(4.65661287307739E-10))       // false
  console.log(xrplValueToNft(12.123))                     // false
  console.log(xrplValueToNft(0.000000000000000000000001)) // false
  console.log('')

  console.log(xrplValueToNft(0.0000000000000000000000000000000000000000000000000000000000000000000001)) // false
  console.log('')
  console.log(xrplValueToNft(0.000000000000000000000000000000000000000000000000000000000000000000000000000000001)) // 1
  console.log('')

  console.log(xrplValueToNft(1000000000000000e-96)) // 1
  console.log(xrplValueToNft(1e-81))                // 1
  console.log(xrplValueToNft(10e-82))               // 1
  console.log('')

  console.log(xrplValueToNft(0.0000000000000000000000000000000000000000000000000000000000000000000000000000001)) // 100
  console.log(xrplValueToNft(1000000000000000e-94)) // 100
  console.log('')

  const someBalance = '3100000000000000e-95' 
  console.log(xrplValueToNft(0.000000000000000000000000000000000000000000000000000000000000000000000000000000031)) // 31
  console.log(xrplValueToNft('0.000000000000000000000000000000000000000000000000000000000000000000000000000000031')) // 31

  console.log(xrplValueToNft(someBalance)) // 31
  console.log(someBalance) // 3100000000000000e-95
  
  // The `nftValueToXrpl` needs the original accountBalance
  // to know the precision for the amount entered (to send)
  console.log(nftValuetoXrpl(31, someBalance)) // 0.000000000000000000000000000000000000000000000000000000000000000000000000000000031
  console.log(nftValuetoXrpl(5)) // 0.000000000000000000000000000000000000000000000000000000000000000000000000000000005
  
  console.log('')

  console.log(xrplValueToNft(-0.000000000000000000000000000000000000000000000000000000000000000000000000000000031)) // -31
  console.log(xrplValueToNft('-1000000000000000e-96')) // -1
  console.log(nftValuetoXrpl(-31, someBalance)) // -0.000000000000000000000000000000000000000000000000000000000000000000000000000000031

  console.log('')