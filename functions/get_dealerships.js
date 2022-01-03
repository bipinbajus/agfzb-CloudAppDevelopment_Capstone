/**
 * Get all dealerships
 */

 const Cloudant = require('@cloudant/cloudant');


 async function main(params) {
     const cloudant = Cloudant({
         url: params.COUCH_URL,
         plugins: { iamauth: { iamApiKey: params.IAM_API_KEY } }
     });
 
 
     try {
         const dbName = 'dealerships'
         let d = await cloudant.use('dealerships').list({include_docs:true})
         
         if(params.state === undefined || params.state === ""){
            return {'data': d.rows}
         }else{
             return { 'data': d.rows.filter(e => e.doc.st === params.state) }
         }
    
     } catch (error) {
         return { error: error.description };
     }
 
 }
