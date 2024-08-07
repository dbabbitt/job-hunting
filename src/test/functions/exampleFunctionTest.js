/* eslint-env mocha */
'use strict'

// tests for exampleFunction
// Generated by serverless-mocha-plugin
const mochaPlugin = require('serverless-mocha-plugin')
const dirtyChai = require('dirty-chai')
mochaPlugin.chai.use(dirtyChai)
const expect = mochaPlugin.chai.expect
let wrapped = mochaPlugin.getWrapper('exampleFunction', '../../../src/functions/exampleFunction.js', 'exampleFunction')
let AWS = require('aws-sdk-mock')
let AWS_SDK = require('aws-sdk')
AWS.setSDKInstance(AWS_SDK)
describe('exampleFunction', () => {
	before((done) => {
		done()
	})
	it('implement tests here', () => {
		return wrapped.run({
			body: JSON.stringify({
				parameter: 'value'
			})
		}).then((response) => {
			expect(response).to.not.be.empty()
		})
	})
})